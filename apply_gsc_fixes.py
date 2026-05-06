"""
Apply Google Search Console verification + SEO/security fixes across all HTML files.
Changes per file:
  1. Insert <meta name="google-site-verification" ...> right after <meta charset="UTF-8">
  2. Update <title> for index.html only
  3. Update <meta name="description"> for index.html only
  4. Add/fix <link rel="canonical"> for each page
  5. Remove the duplicate Font Awesome CDN link in index.html (line 13)
  6. Ensure all internal resource links already use https (they do - style.css and script.js are relative)
"""

import os, re

BASE = r"c:\Users\admin\Desktop\iptv-website"

VERIFICATION = '<meta name="google-site-verification" content="4KImfz50NaUfqPQNmb6E7f7UYEvBwENL8wcPi14IA6k" />'

# Canonical URLs per file
CANONICALS = {
    "index.html":          "https://www.ottoceaniptv.online/",
    "blog.html":           "https://www.ottoceaniptv.online/blog.html",
    "contact.html":        "https://www.ottoceaniptv.online/contact.html",
    "faq.html":            "https://www.ottoceaniptv.online/faq.html",
    "pricing.html":        "https://www.ottoceaniptv.online/pricing.html",
    "blog-post-1.html":    "https://www.ottoceaniptv.online/blog-post-1.html",
    "blog-post-2.html":    "https://www.ottoceaniptv.online/blog-post-2.html",
    "blog-post-3.html":    "https://www.ottoceaniptv.online/blog-post-3.html",
    "blog-post-4.html":    "https://www.ottoceaniptv.online/blog-post-4.html",
    "firestick-guide.html":"https://www.ottoceaniptv.online/firestick-guide.html",
}

# index.html specific overrides
INDEX_TITLE = "OttOcean IPTV | Premium HD & 4K Streaming Service"
INDEX_DESC  = "Enjoy reliable IPTV streaming with 15,000+ live channels and 4K VOD content. Get your 24-hour free trial today."

# Suspicious/duplicate script patterns to remove from index.html (the duplicate FA CDN on line 13)
DUPLICATE_FA_PATTERN = re.compile(
    r'\s*<link rel="stylesheet" href="https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/6\.0\.0/css/all\.min\.css">\r?\n',
    re.MULTILINE
)

results = []

for filename, canonical_url in CANONICALS.items():
    filepath = os.path.join(BASE, filename)
    if not os.path.exists(filepath):
        results.append(f"SKIP (not found): {filename}")
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changes = []

    # ── 1. Add Google site verification after <meta charset="UTF-8"> ──────────
    if 'google-site-verification' not in content:
        # Match the charset meta (with or without trailing whitespace/CRLF)
        content = re.sub(
            r'(<meta charset="UTF-8">)',
            r'\1\n    ' + VERIFICATION,
            content,
            count=1
        )
        changes.append("added google-site-verification")

    # ── 2. Update <title> (index.html only) ──────────────────────────────────
    if filename == "index.html":
        new_title = f"<title>{INDEX_TITLE}</title>"
        content = re.sub(r'<title>[^<]*</title>', new_title, content, count=1)
        changes.append("updated <title>")

    # ── 3. Update <meta name="description"> (index.html only) ────────────────
    if filename == "index.html":
        new_desc = f'<meta name="description" content="{INDEX_DESC}">'
        content = re.sub(
            r'<meta name="description" content="[^"]*">',
            new_desc,
            content,
            count=1
        )
        changes.append("updated meta description")

    # ── 4. Add/update canonical link ─────────────────────────────────────────
    canonical_tag = f'<link rel="canonical" href="{canonical_url}">'

    if 'rel="canonical"' in content:
        # Update existing canonical
        content = re.sub(
            r'<link rel="canonical" href="[^"]*">',
            canonical_tag,
            content,
            count=1
        )
        changes.append("updated canonical link")
    else:
        # Insert before </head>
        content = content.replace('</head>', f'\n{canonical_tag}\n</head>', 1)
        changes.append("added canonical link")

    # ── 5. Remove duplicate/old Font Awesome 6.0.0 link in index.html ────────
    if filename == "index.html":
        new_content = DUPLICATE_FA_PATTERN.sub('', content)
        if new_content != content:
            content = new_content
            changes.append("removed duplicate FA 6.0.0 CDN link")

    # ── Write file if changed ─────────────────────────────────────────────────
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        results.append(f"OK {filename}: {', '.join(changes)}")
    else:
        results.append(f"-- {filename}: no changes needed")

print("\n".join(results))
print("\nDone.")
