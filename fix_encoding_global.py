#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Global encoding fix for OttOcean IPTV website.
Fixes mojibake (corrupted characters) caused by UTF-8 text being
misread/saved as Latin-1 or Windows-1252.

Strategy:
1. Read each file as UTF-8 (with error replacement so we can inspect)
2. Re-encode/decode to recover original characters
3. Apply a curated replacement map for known mojibake patterns
4. Ensure <meta charset="UTF-8"> is present right after <head>
5. Save explicitly as UTF-8 with BOM-less encoding
"""

import os
import re
import sys

# ─── Mojibake replacement map ────────────────────────────────────────────────
# Keys   = corrupted (latin1-mis-decoded) strings as they appear in the file
# Values = correct Unicode characters
REPLACEMENTS = [
    # ── Emoji (4-byte UTF-8 misread as latin1) ──────────────────────────────
    # 💬 WhatsApp / chat bubble  (F0 9F 92 AC)
    ('ðŸ'¬',  '💬'),
    # 🔥 fire  (F0 9F 94 A5)
    ('ðŸ"¥',  '🔥'),
    # 📺 TV  (F0 9F 93 BA)
    ('ðŸ"º',  '📺'),
    # 🎬 clapper / movies  (F0 9F 8E AC)
    ('ðŸŽ¬',  '🎬'),
    # ⚽ soccer ball  (E2 9A BD)
    ('âš½',   '⚽'),
    # ⭐ star  (E2 AD 90)
    ('â­',    '⭐'),
    # ✅ check mark  (E2 9C 85)
    ('âœ…',   '✅'),
    # ❌ cross mark  (E2 9D 8C)
    ('â\u009d\u008c', '❌'),
    # 💳 credit card  (F0 9F 92 B3)
    ('ðŸ'³',  '💳'),
    # 🎁 gift  (F0 9F 8E 81)
    ('ðŸŽ',   '🎁'),
    # 🌟 glowing star  (F0 9F 8C 9F)
    ('ðŸŒŸ',  '🌟'),
    # 📱 mobile phone  (F0 9F 93 B1)
    ('ðŸ"±',  '📱'),
    # 🚀 rocket  (F0 9F 9A 80)
    ('ðŸš€',  '🚀'),
    # 💡 lightbulb  (F0 9F 92 A1)
    ('ðŸ'¡',  '💡'),
    # 🏠 house  (F0 9F 8F A0)
    ('ðŸ\u008f\u00a0', '🏠'),
    # ❓ question mark  (E2 9D 93)
    ('â\u009d\u0093', '❓'),
    # ❗ exclamation  (E2 9D 97)
    ('â\u009d\u0097', '❗'),
    # 👍 thumbs up  (F0 9F 91 8D)
    ('ðŸ'\u008d', '👍'),
    # 👎 thumbs down  (F0 9F 91 8E)
    ('ðŸ'\u008e', '👎'),
    # 🎯 target  (F0 9F 8E AF)
    ('ðŸŽ¯',  '🎯'),
    # 📧 email  (F0 9F 93 A7)
    ('ðŸ"§',  '📧'),
    # 🔗 link  (F0 9F 94 97)
    ('ðŸ"—',  '🔗'),
    # 📝 memo  (F0 9F 93 9D)
    ('ðŸ"\u009d', '📝'),
    # 🌐 globe  (F0 9F 8C 90)
    ('ðŸŒ',   '🌐'),
    # ⚡ lightning  (E2 9A A1)
    ('âš¡',   '⚡'),
    # 💎 diamond  (F0 9F 92 8E)
    ('ðŸ'\u008e', '💎'),
    # 🏆 trophy  (F0 9F 8F 86)
    ('ðŸ\u008f\u0086', '🏆'),
    # 📡 satellite  (F0 9F 93 A1)
    ('ðŸ"¡',  '📡'),
    # 🖥 desktop computer  (F0 9F 96 A5)
    ('ðŸ–¥',  '🖥'),

    # ── Arrows ──────────────────────────────────────────────────────────────
    # → RIGHT ARROW  (E2 86 92)
    ('â†'',   '→'),
    # ← LEFT ARROW  (E2 86 90)
    ('â†\u0090', '←'),
    # ↑ UP ARROW  (E2 86 91)
    ('â†'',   '↑'),
    # ↓ DOWN ARROW  (E2 86 93)
    ('â†"',   '↓'),
    # ➜ HEAVY RIGHT ARROW  (E2 9E 9C)
    ('â\u009e\u009c', '➜'),
    # ➡ RIGHT ARROW  (E2 9E A1)
    ('â\u009e\u00a1', '➡'),
    # ▶ PLAY BUTTON  (E2 96 B6)
    ('â–¶',   '▶'),
    # ◀ BACK BUTTON  (E2 97 80)
    ('â—€',   '◀'),

    # ── Punctuation & Typography ─────────────────────────────────────────────
    # — EM DASH  (E2 80 94)
    ('â€"',   '—'),
    # – EN DASH  (E2 80 93)
    ('â€"',   '–'),
    # ' LEFT SINGLE QUOTATION MARK  (E2 80 98)
    ('â€˜',   '\u2018'),
    # ' RIGHT SINGLE QUOTATION MARK / APOSTROPHE  (E2 80 99)
    ('â€™',   '\u2019'),
    # " LEFT DOUBLE QUOTATION MARK  (E2 80 9C)
    ('â€œ',   '\u201c'),
    # " RIGHT DOUBLE QUOTATION MARK  (E2 80 9D)
    ('â€\u009d', '\u201d'),
    # … ELLIPSIS  (E2 80 A6)
    ('â€¦',   '…'),
    # • BULLET  (E2 80 A2)
    ('â€¢',   '•'),
    # · MIDDLE DOT  (C2 B7)
    ('Â·',    '·'),
    # ‑ NON-BREAKING HYPHEN  (E2 80 91)
    ('â€\u0091', '\u2011'),
    # ™ TRADE MARK  (E2 84 A2)
    ('â„¢',   '™'),
    # © COPYRIGHT  (C2 A9)
    ('Â©',    '©'),
    # ® REGISTERED  (C2 AE)
    ('Â®',    '®'),
    # € EURO SIGN  (E2 82 AC)
    ('â‚¬',   '€'),
    # £ POUND  (C2 A3)
    ('Â£',    '£'),
    # × MULTIPLICATION SIGN  (C3 97)
    ('Ã—',    '×'),
    # ÷ DIVISION SIGN  (C3 B7)
    ('Ã·',    '÷'),
    # ½ ONE HALF  (C2 BD)
    ('Â½',    '½'),
    # ° DEGREE  (C2 B0)
    ('Â°',    '°'),
    # ★ BLACK STAR  (E2 98 85)
    ('â˜…',   '★'),
    # ☆ WHITE STAR  (E2 98 86)
    ('â˜†',   '☆'),
    # ✓ CHECK MARK  (E2 9C 93)
    ('âœ"',   '✓'),
    # ✗ BALLOT X  (E2 9C 97)
    ('âœ—',   '✗'),
    # ✔ HEAVY CHECK MARK  (E2 9C 94)
    ('âœ"',   '✔'),
    # ✖ HEAVY MULTIPLICATION X  (E2 9C 96)
    ('âœ–',   '✖'),
    # « LEFT GUILLEMET  (C2 AB)
    ('Â«',    '«'),
    # » RIGHT GUILLEMET  (C2 BB)
    ('Â»',    '»'),
    # ─ BOX DRAWING  (E2 94 80)
    ('â"€',   '─'),
    # │ BOX DRAWING VERTICAL  (E2 94 82)
    ('â"‚',   '│'),
    # ‐ HYPHEN  (E2 80 90)
    ('â€\u0090', '\u2010'),

    # ── Pricing / Numbers (seen in scan: â€39, â€49, â€65) ─────────────────
    # These appear to be € sign + number  (â‚¬ = €)
    ('â€39',  '€39'),
    ('â€49',  '€49'),
    ('â€65',  '€65'),
    ('â€"39', '€39'),   # alternate corruption
    ('â€"49', '€49'),
    ('â€"65', '€65'),

    # ── Miscellaneous symbols ────────────────────────────────────────────────
    # ── (two em-dashes used as separator, seen in index.html scan)
    ('â€"â€"', '──'),
    # Non-breaking space  (C2 A0)
    ('Â\u00a0', '\u00a0'),
    # Ã (standalone, might be from split Ã© etc.)
    # É  (C3 89)
    ('Ã‰',    'É'),
    # é  (C3 A9)
    ('Ã©',    'é'),
    # à (C3 A0)
    ('Ã ',    'à'),
    # â (C3 A2)
    ('Ã¢',    'â'),
    # ê (C3 AA)
    ('Ãª',    'ê'),
    # î (C3 AE)
    ('Ã®',    'î'),
    # ô (C3 B4)
    ('Ã´',    'ô'),
    # û (C3 BB)
    ('Ã»',    'û'),
    # ü (C3 BC)
    ('Ã¼',    'ü'),
    # ö (C3 B6)
    ('Ã¶',    'ö'),
    # ä (C3 A4)
    ('Ã¤',    'ä'),
]

# Alternative recovery: if the file bytes can be re-decoded
def try_double_decode(text: str) -> str:
    """Attempt to fix text by encoding as latin-1 then decoding as utf-8."""
    try:
        return text.encode('latin-1').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        return text


def apply_replacements(text: str) -> str:
    for bad, good in REPLACEMENTS:
        text = text.replace(bad, good)
    return text


def ensure_utf8_meta(text: str) -> str:
    """Ensure <meta charset="UTF-8"> is the first child of <head>."""
    charset_tag = '<meta charset="UTF-8">'
    charset_variants = [
        '<meta charset="utf-8">',
        '<meta charset="UTF-8">',
        "<meta charset='UTF-8'>",
        "<meta charset='utf-8'>",
        '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"',
        '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"',
    ]

    # Remove any existing charset meta tags
    for variant in charset_variants:
        # Remove full tag (handle self-closing too)
        text = re.sub(re.escape(variant) + r'[^>]*>', '', text, flags=re.IGNORECASE)
        text = re.sub(re.escape(variant), '', text, flags=re.IGNORECASE)

    # Insert right after <head> (case-insensitive)
    text = re.sub(
        r'(<head[^>]*>)',
        r'\1\n    ' + charset_tag,
        text,
        count=1,
        flags=re.IGNORECASE
    )
    return text


def fix_file(filepath: str) -> tuple[bool, str]:
    """Fix encoding in a single file. Returns (changed, summary)."""
    with open(filepath, 'rb') as f:
        raw = f.read()

    # Decode as UTF-8; keep replacement chars for now so we can see them
    text = raw.decode('utf-8', errors='replace')
    original = text

    # Apply string replacements
    text = apply_replacements(text)

    # Ensure charset meta tag
    text = ensure_utf8_meta(text)

    changed = text != original

    if changed:
        # Save back as UTF-8 without BOM
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            f.write(text)

    return changed, filepath


def main():
    cwd = os.path.dirname(os.path.abspath(__file__))
    html_files = [os.path.join(cwd, f) for f in os.listdir(cwd) if f.endswith('.html')]

    print(f"Found {len(html_files)} HTML files to process.\n")

    changed_count = 0
    for fpath in sorted(html_files):
        changed, path = fix_file(fpath)
        fname = os.path.basename(path)
        if changed:
            changed_count += 1
            print(f"  ✔  Fixed: {fname}")
        else:
            print(f"  –  Clean: {fname}")

    print(f"\nDone. {changed_count}/{len(html_files)} files updated.")


if __name__ == '__main__':
    main()
