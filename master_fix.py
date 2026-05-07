#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
master_fix.py - Comprehensive fix for OttOcean IPTV website:
1. Fix comparison table - populate Other Providers column with negative text
2. Fix corrupted/mojibake characters across all HTML files
3. Ensure UTF-8 meta charset is first in head
"""

import os
import re

WORKSPACE = r"c:\Users\admin\Desktop\iptv-website"

# ---------------------------------------------------------------------------
# MOJIBAKE / corrupted-character replacement table
# These are UTF-8 bytes mis-decoded as Latin-1, producing the garbled sequences.
# ---------------------------------------------------------------------------
REPLACEMENTS = [
    # Bullets and separators (â€¢ = U+2022 •)
    ("â€¢", "•"),
    # Em dash (â€" = U+2013 –, â€" = U+2014 —)
    ("â€"", "–"),
    ("â€"", "—"),
    # Left/right double quotes
    ("â€œ", "\u201c"),
    ("â€", "\u201d"),
    # Apostrophe / right single quote
    ("â€™", "\u2019"),
    # Arrow right â†' = →
    ("â†'", "→"),
    # Star ✦ (â˜… or similar)
    ("â˜…", "★"),
    # Euro sign â‚¬ = €
    ("â‚¬", "€"),
    # Registered trademark Â® = ®
    ("Â®", "®"),
    # Non-breaking space Â  = &nbsp;
    ("Â ", "\u00a0"),
    # -- Emoji mojibake sequences --
    # Fire emoji ðŸ"¥
    ("ðŸ"¥", "🔥"),
    # TV ðŸ"º
    ("ðŸ"º", "📺"),
    # Credit card ðŸ'³
    ("ðŸ'³", "💳"),
    # Rocket ðŸš€
    ("ðŸš€", "🚀"),
    # Question mark circle ðŸ'¬
    ("ðŸ'¬", "💬"),
    # Clapper ðŸŽ¬
    ("ðŸŽ¬", "🎬"),
    # Basketball ðŸ€
    ("ðŸ€", "🏀"),
    # Boxing glove ðŸ¥Š
    ("ðŸ¥Š", "🥊"),
    # Globe ðŸŒ
    ("ðŸŒ", "🌐"),
    # Check mark ✔
    ("â€", "✔"),
    # -- Generic replacement character (U+FFFD) rendered as ? box --
    ("\ufffd", ""),
    # "?" used instead of a missing emoji/icon in labels
    # Catch-all: sequences that look like "?" in the label
    ("? Why", "⚡ Why"),
    ("?? OttOcean", "❓ OttOcean"),
    # Marquee tag corruption
    ("?? Global Coverage", "🌍 Global Coverage"),
    # FAQ label
    ("?? OttOcean IPTV FAQ", "❓ OttOcean IPTV FAQ"),
    # "�?" patterns (replacement char + printable)
    ("â€¦", "…"),
    # Double-encoded UTF-8: Ã© = é, etc.
    ("Ã©", "é"),
    ("Ã¨", "è"),
    ("Ã ", "à"),
    ("Ã¢", "â"),
    ("Ã®", "î"),
    ("Ã´", "ô"),
    ("Ã»", "û"),
    ("Ã‡", "Ç"),
    ("Ã‰", "É"),
    # Misc broken sequences in footer/plans: "–" used for price separator
    # e.g. "3 Months – €39" -- we keep the em-dash from the fix above
    # The corrupted "â€"" -> "–" is already covered
    # Option values with corrupted separators
    ("3 Months \ufffd \ufffd39 \ufffd \ufffd39", "3 Months — €39 — €39"),
    ("6 Months \ufffd \ufffd49 \ufffd \ufffd49", "6 Months — €49 — €49"),
    ("12 Months \ufffd \ufffd65 \ufffd \ufffd65", "12 Months — €65 — €65"),
    # Footer plan links
    ("3 Months \ufffd \ufffd39", "3 Months — €39"),
    ("6 Months \ufffd \ufffd49", "6 Months — €49"),
    ("12 Months \ufffd \ufffd65", "12 Months — €65"),
    # db-stream-meta corruption: "4K Ultra HD â€¢ Stable Stream"
    # handled by â€¢ -> • above
    # poster-meta patterns  "4K UHD â€¢ No Buffering â€¢ Sky Sports"
    # handled by â€¢ -> • above
    # "6 Months – Most Popular" badge
    ("6 Months â€"", "6 Months —"),
    # Copyright symbol: © (Â©)
    ("Â©", "©"),
    # Specific corrupted label patterns found in the file
    # "?? Global Coverage" label in marquee
    # Already handled above
    # "? Why OttOcean IPTV?" in comparison section
    # Already handled above
    # Motorsport category with corrupted flag emojis  "🏎 🏁"
    ("ðŸŽ ðŸ", "🏎 🏁"),
    # MMA glove
    ("ðŸ¥Š", "🥊"),
    # Remaining raw replacement chars
    ("\ufffd", ""),
]

# ---------------------------------------------------------------------------
# NEW: Comparison table "Other Providers" column fix
# We'll replace the bare icon-only cells with icon + descriptive negative text
# ---------------------------------------------------------------------------
COMP_REPLACEMENTS = [
    # Streaming Stability
    (
        '<div class="comp-cell"><i class="fas fa-times-circle" style="color: #ef4444; font-size: 1.25rem;"></i></div>\n\n                </div>\n\n                <div class="comp-row">\n\n                    <div class="comp-cell">Support Speed</div>',
        '<div class="comp-cell"><i class="fas fa-times-circle" style="color: #ef4444; margin-right:6px;"></i><span style="font-size:0.82rem;color:#ef4444;font-weight:600;">Frequent Lag &amp; Buffering</span></div>\n\n                </div>\n\n                <div class="comp-row">\n\n                    <div class="comp-cell">Support Speed</div>'
    ),
    # Support Speed
    (
        '<div class="comp-cell"><i class="fas fa-times-circle" style="color: #ef4444; font-size: 1.25rem;"></i></div>\n\n                </div>\n\n                <div class="comp-row">\n\n                    <div class="comp-cell">Channel Quality</div>',
        '<div class="comp-cell"><i class="fas fa-times-circle" style="color: #ef4444; margin-right:6px;"></i><span style="font-size:0.82rem;color:#ef4444;font-weight:600;">Slow Email Tickets (24h+)</span></div>\n\n                </div>\n\n                <div class="comp-row">\n\n                    <div class="comp-cell">Channel Quality</div>'
    ),
    # Channel Quality
    (
        '<div class="comp-cell"><i class="fas fa-times-circle" style="color: #ef4444; font-size: 1.25rem;"></i></div>\n\n                </div>\n\n                <div class="comp-row">\n\n                    <div class="comp-cell">Anti-Freeze 10.0</div>',
        '<div class="comp-cell"><i class="fas fa-times-circle" style="color: #ef4444; margin-right:6px;"></i><span style="font-size:0.82rem;color:#ef4444;font-weight:600;">Compressed HD/SD Only</span></div>\n\n                </div>\n\n                <div class="comp-row">\n\n                    <div class="comp-cell">Anti-Freeze 10.0</div>'
    ),
    # Anti-Freeze 10.0
    (
        '<div class="comp-cell"><i class="fas fa-times-circle" style="color: #ef4444; font-size: 1.25rem;"></i></div>\n\n                </div>\n\n            </div>\n\n        </div>\n\n    </section>\n\n\n\n    <section id="pricing">',
        '<div class="comp-cell"><i class="fas fa-times-circle" style="color: #ef4444; margin-right:6px;"></i><span style="font-size:0.82rem;color:#ef4444;font-weight:600;">Not Included</span></div>\n\n                </div>\n\n            </div>\n\n        </div>\n\n    </section>\n\n\n\n    <section id="pricing">'
    ),
]

# ---------------------------------------------------------------------------
# Specific label fixes using exact substring matching
# ---------------------------------------------------------------------------
LABEL_FIXES = [
    # Marquee section label
    ('class="marquee-tag">\ufffd\ufffd Global Coverage<', 'class="marquee-tag">🌍 Global Coverage<'),
    ('class="marquee-tag">?? Global Coverage<', 'class="marquee-tag">🌍 Global Coverage<'),
    # Comparison section label
    ('class="categories-label">? Why OttOcean IPTV?<', 'class="categories-label">⚡ Why OttOcean IPTV?<'),
    # FAQ section label
    ('class="faq-label"', 'class="faq-label"'),  # no-op placeholder
    ('>?? OttOcean IPTV FAQ<', '>❓ OttOcean IPTV FAQ<'),
    # Hero sub text
    ('15,000+ Channels, 4K Quality \ufffd the ultimate', '15,000+ Channels, 4K Quality — the ultimate'),
    ('15,000+ Channels, 4K Quality ? the ultimate', '15,000+ Channels, 4K Quality — the ultimate'),
    # Stream meta
    ('4K Ultra HD \ufffd Stable Stream<', '4K Ultra HD • Stable Stream<'),
    ('4K Ultra HD ? Stable Stream<', '4K Ultra HD • Stable Stream<'),
    # Poster metas
    ('4K UHD \ufffd No Buffering \ufffd Sky Sports<', '4K UHD • No Buffering • Sky Sports<'),
    ('HD \ufffd ESPN<', 'HD • ESPN<'),
    ('HD \ufffd BT Sport<', 'HD • BT Sport<'),
    ('4K \ufffd Sky Sports F1<', '4K • Sky Sports F1<'),
    ('4K \ufffd ESPN PPV<', '4K • ESPN PPV<'),
    ('40,000+ Titles \ufffd Updated Daily<', '40,000+ Titles • Updated Daily<'),
    ('HBO \ufffd Netflix \ufffd Disney+<', 'HBO • Netflix • Disney+<'),
    ('4K UHD \ufffd Dolby Vision<', '4K UHD • Dolby Vision<'),
    ('HD \ufffd Prime Video<', 'HD • Prime Video<'),
    ('HD \ufffd Hulu \ufffd Peacock<', 'HD • Hulu • Peacock<'),
    # Footer tagline
    ('Premium IPTV streaming \ufffd 15,000+ channels', 'Premium IPTV streaming • 15,000+ channels'),
    ('Premium IPTV streaming ? 15,000+ channels', 'Premium IPTV streaming • 15,000+ channels'),
    # Copyright
    ('\ufffd <span id="footer-year">', '© <span id="footer-year">'),
    ('? <span id="footer-year">', '© <span id="footer-year">'),
    # Select options with corrupted separators
    ('>3 Months \ufffd \ufffd39 \ufffd \ufffd39<', '>3 Months — €39<'),
    ('>6 Months \ufffd \ufffd49 \ufffd \ufffd49<', '>6 Months — €49<'),
    ('>12 Months \ufffd \ufffd65 \ufffd \ufffd65<', '>12 Months — €65<'),
    # Footer plan links
    ('>3 Months \ufffd \ufffd39<', '>3 Months — €39<'),
    ('>6 Months \ufffd \ufffd49<', '>6 Months — €49<'),
    ('>12 Months \ufffd \ufffd65<', '>12 Months — €65<'),
    # Basket sport label
    ('>?? Basketball<', '>🏀 Basketball<'),
    ('>? ? Motorsport<', '>🏎 🏁 Motorsport<'),
    # MMA
    ('>?? MMA<', '>🥊 MMA<'),
]


def fix_meta_charset(content: str) -> str:
    """Ensure <meta charset="UTF-8"> is the FIRST tag inside <head>."""
    # Remove any existing charset meta (wherever it appears)
    content = re.sub(r'\s*<meta\s+charset=["\']UTF-8["\']\s*/?>', '', content, flags=re.IGNORECASE)
    # Insert immediately after <head>
    content = re.sub(r'(<head>)', r'\1\n    <meta charset="UTF-8">', content, flags=re.IGNORECASE)
    return content


def apply_label_fixes(content: str) -> str:
    for old, new in LABEL_FIXES:
        content = content.replace(old, new)
    return content


def apply_mojibake_fixes(content: str) -> str:
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)
    return content


def fix_comp_table_index(content: str) -> str:
    """
    In index.html specifically, fix the Other Providers column cells
    to include descriptive negative text alongside the red X icon.
    We do this by targeting exact patterns.
    """
    # Pattern: comp-cell with only times-circle icon, no text
    # Replace them in order (streaming, support, channel, antifreeze)
    rows_data = [
        ("Streaming Stability", "Frequent Lag &amp; Buffering"),
        ("Support Speed",        "Slow Email Tickets (24h+)"),
        ("Channel Quality",      "Compressed HD/SD Only"),
        ("Anti-Freeze 10.0",     "Not Included"),
    ]

    # We'll process row by row using a state machine approach
    result = content
    for feature, negative_text in rows_data:
        # Find the row for this feature
        # Pattern: comp-cell with feature name -> highlighted cell -> bare icon cell
        # The bare icon-only comp-cell pattern:
        bare_icon_pattern = (
            r'(<div class="comp-cell">'
            r'<i class="fas fa-times-circle" style="color: #ef4444; font-size: 1\.25rem;"></i>'
            r'</div>)'
        )
        replacement = (
            '<div class="comp-cell">'
            '<i class="fas fa-times-circle" style="color: #ef4444; margin-right:6px;"></i>'
            f'<span style="font-size:0.82rem;color:#ef4444;font-weight:600;">{negative_text}</span>'
            '</div>'
        )
        # Find the section containing this feature row
        # Locate the feature name in a comp-cell, then find the next bare icon cell
        feature_pos = result.find(f'<div class="comp-cell">{feature}</div>')
        if feature_pos == -1:
            continue
        # Search for the bare icon pattern after the feature position
        sub = result[feature_pos:]
        m = re.search(bare_icon_pattern, sub)
        if m:
            # Replace only this first occurrence after feature_pos
            result = result[:feature_pos] + sub[:m.start()] + replacement + sub[m.end():]
    return result


def process_file(fpath: str):
    with open(fpath, 'rb') as fh:
        raw = fh.read()

    # Decode – try UTF-8 first, fallback to latin-1
    try:
        content = raw.decode('utf-8')
    except UnicodeDecodeError:
        content = raw.decode('latin-1')
        print(f"  [WARNING] {os.path.basename(fpath)} decoded as latin-1")

    original = content

    # 1. Apply mojibake character fixes
    content = apply_mojibake_fixes(content)

    # 2. Apply label-specific fixes
    content = apply_label_fixes(content)

    # 3. Fix charset meta placement
    content = fix_meta_charset(content)

    # 4. Fix comparison table (index.html only)
    if os.path.basename(fpath) == 'index.html':
        content = fix_comp_table_index(content)

    if content != original:
        with open(fpath, 'w', encoding='utf-8', newline='') as fh:
            fh.write(content)
        print(f"  [FIXED]   {os.path.basename(fpath)}")
    else:
        print(f"  [OK]      {os.path.basename(fpath)} (no changes needed)")


def main():
    print("=" * 60)
    print("OttOcean IPTV - Master Fix Script")
    print("=" * 60)
    html_files = [
        os.path.join(WORKSPACE, f)
        for f in os.listdir(WORKSPACE)
        if f.endswith('.html')
    ]
    for fpath in sorted(html_files):
        process_file(fpath)
    print("=" * 60)
    print("Done.")


if __name__ == '__main__':
    main()
