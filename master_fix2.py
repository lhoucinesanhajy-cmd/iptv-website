#!/usr/bin/env python3
# coding: utf-8
"""
master_fix2.py - OttOcean IPTV comprehensive fix script
Fixes: encoding/mojibake, comparison table, charset meta placement
"""

import os
import re

WORKSPACE = r"c:\Users\admin\Desktop\iptv-website"

# Mojibake replacement pairs: (corrupted_str, correct_unicode)
# All strings use only ASCII or explicit \u escapes to avoid file-save issues
REPLACEMENTS = [
    # Bullet U+2022
    ("\u00e2\u0080\u00a2", "\u2022"),
    # En-dash U+2013
    ("\u00e2\u0080\u0093", "\u2013"),
    # Em-dash U+2014
    ("\u00e2\u0080\u0094", "\u2014"),
    # Left double-quote U+201C
    ("\u00e2\u0080\u009c", "\u201c"),
    # Right double-quote U+201D
    ("\u00e2\u0080\u009d", "\u201d"),
    # Right single-quote / apostrophe U+2019
    ("\u00e2\u0080\u0099", "\u2019"),
    # Arrow right U+2192
    ("\u00e2\u0086\u0092", "\u2192"),
    # Black star U+2605
    ("\u00e2\u0098\u0085", "\u2605"),
    # Euro sign U+20AC
    ("\u00e2\u0082\u00ac", "\u20ac"),
    # Registered TM U+00AE
    ("\u00c2\u00ae", "\u00ae"),
    # Copyright U+00A9
    ("\u00c2\u00a9", "\u00a9"),
    # Non-breaking space
    ("\u00c2\u00a0", "\u00a0"),
    # Ellipsis U+2026
    ("\u00e2\u0080\u00a6", "\u2026"),
    # Fire emoji U+1F525
    ("\u00f0\u009f\u0094\u00a5", "\U0001f525"),
    # TV emoji U+1F4FA
    ("\u00f0\u009f\u0093\u00ba", "\U0001f4fa"),
    # Credit card U+1F4B3
    ("\u00f0\u009f\u0092\u00b3", "\U0001f4b3"),
    # Rocket U+1F680
    ("\u00f0\u009f\u009a\u0080", "\U0001f680"),
    # Speech bubble U+1F4AC
    ("\u00f0\u009f\u0092\u00ac", "\U0001f4ac"),
    # Clapper U+1F3AC
    ("\u00f0\u009f\u008e\u00ac", "\U0001f3ac"),
    # Basketball U+1F3C0
    ("\u00f0\u009f\u008f\u0080", "\U0001f3c0"),
    # Boxing glove U+1F94A
    ("\u00f0\u009f\u00a5\u008a", "\U0001f94a"),
    # Globe U+1F310
    ("\u00f0\u009f\u008c\u0090", "\U0001f310"),
    # é
    ("\u00c3\u00a9", "\u00e9"),
    # è
    ("\u00c3\u00a8", "\u00e8"),
    # à
    ("\u00c3\u00a0", "\u00e0"),
    # â
    ("\u00c3\u00a2", "\u00e2"),
    # Unicode replacement char -> remove
    ("\ufffd", ""),
]

# Label-specific fixes applied AFTER mojibake fixes
# Using only printable ASCII or \u escapes
LABEL_FIXES = [
    # Marquee global coverage label
    ('class="marquee-tag">?? Global Coverage<',
     'class="marquee-tag">\U0001f30d Global Coverage<'),
    ('class="marquee-tag">\ufffd\ufffd Global Coverage<',
     'class="marquee-tag">\U0001f30d Global Coverage<'),
    # Comparison section label
    ('class="categories-label">? Why OttOcean IPTV?<',
     'class="categories-label">\u26a1 Why OttOcean IPTV?<'),
    # FAQ label
    ('>?? OttOcean IPTV FAQ<',
     '>\u2753 OttOcean IPTV FAQ<'),
    ('>?\u200b\u200b OttOcean IPTV FAQ<',
     '>\u2753 OttOcean IPTV FAQ<'),
    # Hero sub text - bullet separator
    ('4K Quality \ufffd the ultimate',
     '4K Quality \u2014 the ultimate'),
    ('4K Quality ? the ultimate',
     '4K Quality \u2014 the ultimate'),
    # Stream meta bullets
    ('4K Ultra HD \ufffd Stable Stream',
     '4K Ultra HD \u2022 Stable Stream'),
    ('4K Ultra HD ? Stable Stream',
     '4K Ultra HD \u2022 Stable Stream'),
    # Poster metas
    ('4K UHD \ufffd No Buffering \ufffd Sky Sports',
     '4K UHD \u2022 No Buffering \u2022 Sky Sports'),
    ('HD \ufffd ESPN', 'HD \u2022 ESPN'),
    ('HD \ufffd BT Sport', 'HD \u2022 BT Sport'),
    ('4K \ufffd Sky Sports F1', '4K \u2022 Sky Sports F1'),
    ('4K \ufffd ESPN PPV', '4K \u2022 ESPN PPV'),
    ('40,000+ Titles \ufffd Updated Daily', '40,000+ Titles \u2022 Updated Daily'),
    ('HBO \ufffd Netflix \ufffd Disney+', 'HBO \u2022 Netflix \u2022 Disney+'),
    ('4K UHD \ufffd Dolby Vision', '4K UHD \u2022 Dolby Vision'),
    ('HD \ufffd Prime Video', 'HD \u2022 Prime Video'),
    ('HD \ufffd Hulu \ufffd Peacock', 'HD \u2022 Hulu \u2022 Peacock'),
    # Footer tagline
    ('Premium IPTV streaming \ufffd 15,000+',
     'Premium IPTV streaming \u2022 15,000+'),
    ('Premium IPTV streaming ? 15,000+',
     'Premium IPTV streaming \u2022 15,000+'),
    # Copyright in footer
    ('\ufffd <span id="footer-year">',
     '\u00a9 <span id="footer-year">'),
    ('? <span id="footer-year">',
     '\u00a9 <span id="footer-year">'),
    # Select option price separators
    ('>3 Months \ufffd \ufffd39 \ufffd \ufffd39<',
     '>3 Months \u2014 \u20ac39<'),
    ('>6 Months \ufffd \ufffd49 \ufffd \ufffd49<',
     '>6 Months \u2014 \u20ac49<'),
    ('>12 Months \ufffd \ufffd65 \ufffd \ufffd65<',
     '>12 Months \u2014 \u20ac65<'),
    # Footer plan links
    ('>3 Months \ufffd \ufffd39<', '>3 Months \u2014 \u20ac39<'),
    ('>6 Months \ufffd \ufffd49<', '>6 Months \u2014 \u20ac49<'),
    ('>12 Months \ufffd \ufffd65<', '>12 Months \u2014 \u20ac65<'),
    # Basket sport label
    ('>?? Basketball<', '>\U0001f3c0 Basketball<'),
    ('>?? Motorsport<', '>\U0001f3ce \U0001f3c1 Motorsport<'),
    ('>? ??  Motorsport<', '>\U0001f3ce \U0001f3c1 Motorsport<'),
    ('>? ??  Motorsport<', '>\U0001f3ce \U0001f3c1 Motorsport<'),
    ('>?? MMA<', '>\U0001f94a MMA<'),
    # "–" in 6 Months badge  "6 Months –"
    ('6 Months \u00e2\u0080\u0093 Most Popular',
     '6 Months \u2013 Most Popular'),
]


def fix_meta_charset(content):
    """Remove existing charset meta anywhere, add it first inside <head>."""
    content = re.sub(
        r'\s*<meta\s+charset=["\']UTF-8["\']\s*/?>\s*',
        '',
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(
        r'(<head>)',
        r'\1\n    <meta charset="UTF-8">',
        content,
        count=1,
        flags=re.IGNORECASE
    )
    return content


def fix_comp_table(content):
    """
    Replace bare icon-only comp-cells in the Other Providers column
    with icon + descriptive negative text.
    """
    rows_data = [
        ("Streaming Stability", "Frequent Lag &amp; Buffering"),
        ("Support Speed",        "Slow Email Tickets (24h+)"),
        ("Channel Quality",      "Compressed HD/SD Only"),
        ("Anti-Freeze 10.0",     "Not Included"),
    ]

    bare_icon_re = re.compile(
        r'<div class="comp-cell">'
        r'\s*<i class="fas fa-times-circle"[^>]*></i>\s*'
        r'</div>'
    )

    for feature, negative_text in rows_data:
        feature_pos = content.find(
            '<div class="comp-cell">{}</div>'.format(feature)
        )
        if feature_pos == -1:
            continue
        sub = content[feature_pos:]
        m = bare_icon_re.search(sub)
        if m:
            replacement = (
                '<div class="comp-cell">'
                '<i class="fas fa-times-circle" style="color: #ef4444; margin-right:6px;"></i>'
                '<span style="font-size:0.82rem;color:#ef4444;font-weight:600;">'
                '{}</span></div>'.format(negative_text)
            )
            content = (
                content[:feature_pos]
                + sub[:m.start()]
                + replacement
                + sub[m.end():]
            )
    return content


def process_file(fpath):
    fname = os.path.basename(fpath)
    with open(fpath, 'rb') as fh:
        raw = fh.read()

    try:
        content = raw.decode('utf-8')
        encoding_used = 'utf-8'
    except UnicodeDecodeError:
        content = raw.decode('latin-1')
        encoding_used = 'latin-1'
        print(f"  [WARN] {fname}: decoded as latin-1")

    original = content

    # Step 1: mojibake
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)

    # Step 2: label-specific
    for old, new in LABEL_FIXES:
        content = content.replace(old, new)

    # Step 3: charset meta
    content = fix_meta_charset(content)

    # Step 4: comparison table (index.html only)
    if fname == 'index.html':
        content = fix_comp_table(content)

    if content != original:
        with open(fpath, 'w', encoding='utf-8', newline='\r\n') as fh:
            fh.write(content)
        print(f"  [FIXED]  {fname}")
    else:
        print(f"  [OK]     {fname} (no changes)")


def main():
    print("=" * 55)
    print("OttOcean IPTV - Master Fix Script v2")
    print("=" * 55)
    html_files = sorted(
        os.path.join(WORKSPACE, f)
        for f in os.listdir(WORKSPACE)
        if f.endswith('.html')
    )
    for fpath in html_files:
        process_file(fpath)
    print("=" * 55)
    print("All done.")


if __name__ == '__main__':
    main()
