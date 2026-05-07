#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_mojibake.py – Global UTF-8 encoding fix for the OttOcean IPTV website.

Strategy:
1. Read every file as raw bytes.
2. Decode with latin-1 (which is lossless for any byte sequence).
3. Re-encode to latin-1 bytes, then decode as UTF-8 to undo the double-encode.
4. If that still leaves leftover mojibake sequences, apply a manual replacement table.
5. Write the result back as UTF-8 (no BOM).
"""

import os
import re

WORKSPACE = r"c:\Users\admin\Desktop\iptv-website"

# ── Manual replacement table for known mojibake → correct UTF-8 ──────────────
# These are the most common Windows-1252 / Latin-1 misread sequences.
REPLACEMENTS = [
    # Emojis (UTF-8 bytes misread as Latin-1)
    ("ðŸ"¥",  "🔥"),  # fire
    ("ðŸ"º",  "📺"),  # TV
    ("ðŸŒ",   "🌍"),  # globe
    ("ðŸŽ¬",  "🎬"),  # clapper
    ("ðŸ'¬",  "💬"),  # speech bubble
    ("ðŸ'",   "👍"),  # thumbs up
    ("ðŸ'Ž",  "👎"),  # thumbs down
    ("ðŸ'€",  "👀"),  # eyes
    ("ðŸ†",  "🏆"),  # trophy
    ("ðŸŽ",   "🎁"),  # gift
    ("ðŸ"",   "🔍"),  # magnifier
    ("ðŸ"±",  "📱"),  # phone
    ("ðŸ'»",  "💻"),  # laptop
    ("ðŸŒŸ",  "🌟"),  # glowing star
    ("â­",   "⭐"),  # star (standalone)
    ("â­•",   "⭕"),  # circle
    ("â†'",   "→"),   # right arrow
    ("â†"",   "↔"),   # left-right arrow
    ("â†"",   "↓"),   # down arrow
    ("â†",    "←"),   # left arrow
    ("â†'",   "↑"),   # up arrow
    ("â€"",   "—"),   # em dash
    ("â€"",   "–"),   # en dash
    ("â€˜",   "\u2018"),  # left single quote
    ("â€™",   "\u2019"),  # right single quote / apostrophe
    ("â€œ",   "\u201C"),  # left double quote
    ("â€",    "\u201D"),  # right double quote
    ("â€¦",   "…"),   # ellipsis
    ("â€¢",   "•"),   # bullet
    ("â„¢",   "™"),   # trade mark
    ("Â©",    "©"),   # copyright
    ("Â®",    "®"),   # registered
    ("Â°",    "°"),   # degree
    ("Ã©",    "é"),
    ("Ã¨",    "è"),
    ("Ã ",    "à"),
    ("Ã¢",    "â"),
    ("Ã®",    "î"),
    ("Ã´",    "ô"),
    ("Ã»",    "û"),
    ("Ã§",    "ç"),
    ("Ã«",    "ë"),
    ("Ã¯",    "ï"),
    ("Ã¼",    "ü"),
    ("Ã¶",    "ö"),
    ("Ã¤",    "ä"),
    ("Ã±",    "ñ"),
    ("â‚¬",   "€"),   # euro sign
    ("Â£",    "£"),   # pound
    ("Â¥",    "¥"),   # yen
    # Star ratings
    ("â˜…",   "★"),
    ("â˜†",   "☆"),
    # Check/cross
    ("âœ"",    "✔"),
    ("âœ—",    "✗"),
    ("âœ…",    "✅"),
    ("âŒ",    "❌"),
    # WhatsApp / chat
    ("ðŸ'¬",  "💬"),
    # Additional common ones
    ("Â·",    "·"),
    ("Â»",    "»"),
    ("Â«",    "«"),
]

# Extensions to process
EXTENSIONS = {".html", ".css", ".js", ".txt", ".xml"}

def fix_content(content_str: str) -> str:
    """Try auto-fix via double-decode, then apply manual table."""
    # Method 1: attempt double-decode (Latin-1 → bytes → UTF-8)
    try:
        fixed = content_str.encode("latin-1").decode("utf-8")
        content_str = fixed
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass  # If it fails, the manual table below will still clean things up.

    # Method 2: Manual replacement table
    for bad, good in REPLACEMENTS:
        content_str = content_str.replace(bad, good)

    return content_str

def ensure_utf8_meta(content: str, filepath: str) -> str:
    """Ensure <meta charset="UTF-8"> is the very first tag inside <head>."""
    if not filepath.endswith(".html"):
        return content

    # Remove any existing charset meta (wherever it is)
    content = re.sub(
        r'<meta\s+charset=["\']?[^"\'>\s]+["\']?\s*/?>',
        '',
        content,
        flags=re.IGNORECASE
    )

    # Insert right after <head>
    content = re.sub(
        r'(<head[^>]*>)',
        r'\1\n    <meta charset="UTF-8">',
        content,
        count=1,
        flags=re.IGNORECASE
    )
    return content

def process_file(filepath: str):
    ext = os.path.splitext(filepath)[1].lower()
    if ext not in EXTENSIONS:
        return

    # Read raw bytes – try UTF-8 first, fall back to latin-1
    with open(filepath, "rb") as f:
        raw = f.read()

    # Strip UTF-8 BOM if present
    if raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]

    # Decode using latin-1 (lossless) so we can inspect the characters
    content_latin = raw.decode("latin-1")

    # Apply fixes
    fixed = fix_content(content_latin)

    # Ensure charset meta for HTML
    fixed = ensure_utf8_meta(fixed, filepath)

    # Write back as UTF-8 without BOM, using CRLF line endings (Windows)
    out_bytes = fixed.encode("utf-8")
    with open(filepath, "wb") as f:
        f.write(out_bytes)

    print(f"  ✔ Fixed: {os.path.basename(filepath)}")

def main():
    print("=" * 60)
    print("OttOcean IPTV – Global Mojibake Fix")
    print("=" * 60)

    count = 0
    for root, dirs, files in os.walk(WORKSPACE):
        # Skip .git and other hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext in EXTENSIONS:
                fpath = os.path.join(root, fname)
                process_file(fpath)
                count += 1

    print()
    print(f"Done! Processed {count} files.")

if __name__ == "__main__":
    main()
