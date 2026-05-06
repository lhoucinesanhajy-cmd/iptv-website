#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Global UTF-8 encoding fix for OttOcean IPTV website.
- Ensures <meta charset="UTF-8"> is first in <head>
- Replaces all broken mojibake strings with correct UTF-8 characters
"""

import os
import re

HTML_FILES = [
    "index.html",
    "blog.html",
    "blog-post-1.html",
    "blog-post-2.html",
    "blog-post-3.html",
    "blog-post-4.html",
    "contact.html",
    "faq.html",
    "firestick-guide.html",
    "pricing.html",
]

# Mojibake: UTF-8 bytes read as Latin-1/Windows-1252
# Each tuple: (broken_string, correct_string)
REPLACEMENTS = [
    # --- Emoji ---
    ("\u00f0\u009f\u0092\u00ac", "\U0001f4ac"),   # speech bubble
    ("\u00f0\u009f\u0093\u009e", "\U0001f4de"),   # telephone receiver
    ("\u00f0\u009f\u0093\u00b1", "\U0001f4f1"),   # mobile phone
    ("\u00f0\u009f\u008e\u00af", "\U0001f3af"),   # target
    ("\u00f0\u009f\u008c\u008a", "\U0001f30a"),   # wave
    ("\u00e2\u009a\u00a1", "\u26a1"),              # lightning bolt
    ("\u00f0\u009f\u0093\u00ba", "\U0001f4fa"),   # television
    ("\u00f0\u009f\u008e\u00ac", "\U0001f3ac"),   # movie clapper
    ("\u00f0\u009f\u008f\u0086", "\U0001f3c6"),   # trophy
    ("\u00f0\u009f\u009a\u0080", "\U0001f680"),   # rocket
    ("\u00f0\u009f\u0091\u008d", "\U0001f44d"),   # thumbs up
    ("\u00f0\u009f\u0094\u00a5", "\U0001f525"),   # fire
    ("\u00e2\u00ad\u0090", "\u2b50"),              # star
    ("\u00f0\u009f\u008c\u008d", "\U0001f30d"),   # globe
    ("\u00f0\u009f\u008e\u0081", "\U0001f381"),   # gift
    ("\u00f0\u009f\u0092\u00b0", "\U0001f4b0"),   # money bag
    ("\u00f0\u009f\u0094\u0091", "\U0001f511"),   # key
    ("\u00f0\u009f\u009b\u00a1", "\U0001f6e1"),   # shield
    ("\u00f0\u009f\u008e\u0096", "\U0001f3d6"),   # beach
    ("\u00f0\u009f\u0092\u008e", "\U0001f48e"),   # gem
    ("\u00f0\u009f\u0093\u008a", "\U0001f4ca"),   # bar chart
    ("\u00f0\u009f\u00a4\u009d", "\U0001f91d"),   # handshake
    ("\u00f0\u009f\u0094\u00a7", "\U0001f527"),   # wrench
    ("\u00f0\u009f\u0092\u00bb", "\U0001f4bb"),   # laptop
    ("\u00f0\u009f\u0096\u00a5", "\U0001f5a5"),   # desktop computer
    ("\u00f0\u009f\u0093\u00a1", "\U0001f4e1"),   # satellite
    ("\u00f0\u009f\u0083\u00b0", "\U0001f0f0"),   # (card)
    ("\u00e2\u009a\u00bd", "\u26bd"),              # soccer ball
    ("\u00f0\u009f\u008f\u0088", "\U0001f3c8"),   # american football
    ("\u00f0\u009f\u008e\u00ae", "\U0001f3ae"),   # video game
    ("\u00f0\u009f\u0099\u008c", "\U0001f64c"),   # raising hands
    ("\u00f0\u009f\u0091\u008f", "\U0001f44f"),   # clapping
    ("\u00f0\u009f\u00a5\u0087", "\U0001f947"),   # gold medal
    ("\u00f0\u009f\u00a5\u0088", "\U0001f948"),   # silver medal
    ("\u00f0\u009f\u00a5\u0089", "\U0001f949"),   # bronze medal
    ("\u00f0\u009f\u008f\u00a0", "\U0001f3e0"),   # house
    ("\u00f0\u009f\u008f\u00a1", "\U0001f3e1"),   # house with garden
    ("\u00f0\u009f\u008f\u00a2", "\U0001f3e2"),   # office building
    ("\u00f0\u009f\u0098\u008a", "\U0001f60a"),   # smiling face
    ("\u00f0\u009f\u0098\u008d", "\U0001f60d"),   # heart eyes
    ("\u00f0\u009f\u0091\u008b", "\U0001f44b"),   # waving hand

    # --- Currency ---
    ("\u00e2\u0082\u00ac", "\u20ac"),   # Euro sign €
    ("\u00c2\u00a3", "\u00a3"),         # Pound sign £
    ("\u00c2\u00a5", "\u00a5"),         # Yen sign ¥
    ("\u00c2\u00a9", "\u00a9"),         # Copyright ©
    ("\u00c2\u00ae", "\u00ae"),         # Registered ®
    ("\u00e2\u0084\u00a2", "\u2122"),   # Trademark ™

    # --- Dashes and punctuation ---
    ("\u00e2\u0080\u0093", "\u2013"),   # en dash –
    ("\u00e2\u0080\u0094", "\u2014"),   # em dash —
    ("\u00e2\u0080\u0099", "\u2019"),   # right single quote '
    ("\u00e2\u0080\u0098", "\u2018"),   # left single quote '
    ("\u00e2\u0080\u009c", "\u201c"),   # left double quote "
    ("\u00e2\u0080\u009d", "\u201d"),   # right double quote "
    ("\u00e2\u0080\u00a6", "\u2026"),   # ellipsis …
    ("\u00c2\u00ab", "\u00ab"),         # left angle quote «
    ("\u00c2\u00bb", "\u00bb"),         # right angle quote »
    ("\u00e2\u0080\u00a2", "\u2022"),   # bullet •
    ("\u00c2\u00b7", "\u00b7"),         # middle dot ·

    # --- Arrows ---
    ("\u00e2\u0086\u0092", "\u2192"),   # right arrow →
    ("\u00e2\u0086\u0090", "\u2190"),   # left arrow ←
    ("\u00e2\u0086\u0091", "\u2191"),   # up arrow ↑
    ("\u00e2\u0086\u0093", "\u2193"),   # down arrow ↓

    # --- Check marks ---
    ("\u00e2\u009c\u0093", "\u2713"),   # check mark ✓
    ("\u00e2\u009c\u0094", "\u2714"),   # heavy check mark ✔
    ("\u00e2\u009c\u0096", "\u2716"),   # heavy multiplication x ✖
    ("\u00e2\u009c\u0097", "\u2717"),   # ballot x ✗

    # --- Accented characters ---
    ("\u00c3\u00a9", "\u00e9"),   # é
    ("\u00c3\u00a8", "\u00e8"),   # è
    ("\u00c3\u00a0", "\u00e0"),   # à
    ("\u00c3\u00a2", "\u00e2"),   # â
    ("\u00c3\u00af", "\u00ef"),   # ï
    ("\u00c3\u00ae", "\u00ee"),   # î
    ("\u00c3\u00b4", "\u00f4"),   # ô
    ("\u00c3\u00b9", "\u00f9"),   # ù
    ("\u00c3\u00bb", "\u00fb"),   # û
    ("\u00c3\u00a7", "\u00e7"),   # ç
    ("\u00c3\u00ab", "\u00eb"),   # ë
    ("\u00c3\u00a6", "\u00e6"),   # æ
    ("\u00c3\u00a4", "\u00e4"),   # ä
    ("\u00c3\u00b6", "\u00f6"),   # ö
    ("\u00c3\u00bc", "\u00fc"),   # ü
    ("\u00c3\u00b1", "\u00f1"),   # ñ

    # --- Non-breaking space ---
    ("\u00c2\u00a0", "\u00a0"),   # NBSP
]


def ensure_charset_meta(content):
    """Ensure <meta charset='UTF-8'> is the very first tag inside <head>."""
    # Remove any existing charset meta tags (various forms)
    content = re.sub(
        r'<meta\s+charset=["\']?[^"\'>\s]+["\']?\s*/?>',
        '',
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(
        r'<meta\s+http-equiv=["\']?content-type["\']?[^>]*>',
        '',
        content,
        flags=re.IGNORECASE
    )
    # Insert immediately after <head ...>
    content = re.sub(
        r'(<head[^>]*>)',
        r'\1\n    <meta charset="UTF-8">',
        content,
        count=1,
        flags=re.IGNORECASE
    )
    return content


def apply_replacements(content):
    """Apply all mojibake replacements."""
    for broken, fixed in REPLACEMENTS:
        if broken in content:
            content = content.replace(broken, fixed)
    return content


def fix_file(filepath):
    """Read, fix, and write a single HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print("  ERROR reading {}: {}".format(filepath, e))
        return False

    original = content

    # Step 1: Character replacements first
    content = apply_replacements(content)

    # Step 2: Ensure charset meta is first in <head>
    content = ensure_charset_meta(content)

    if content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print("  Fixed: {}".format(filepath))
        except Exception as e:
            print("  ERROR writing {}: {}".format(filepath, e))
            return False
    else:
        print("  No changes needed: {}".format(filepath))

    return True


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    print("=" * 60)
    print("OttOcean IPTV - Global UTF-8 Encoding Fix")
    print("=" * 60)

    fixed_count = 0
    for fname in HTML_FILES:
        if os.path.exists(fname):
            print("\nProcessing: {}".format(fname))
            if fix_file(fname):
                fixed_count += 1
        else:
            print("\n  SKIP (not found): {}".format(fname))

    print("\n" + "=" * 60)
    print("Done! Processed {}/{} files.".format(fixed_count, len(HTML_FILES)))
    print("=" * 60)


if __name__ == "__main__":
    main()
