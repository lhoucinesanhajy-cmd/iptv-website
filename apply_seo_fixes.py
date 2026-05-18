import os
import re

BASE_DIR = r"c:\Users\admin\Desktop\iptv-website"
SITEMAP_FILE = os.path.join(BASE_DIR, "sitemap.xml")

html_files = []
for root, dirs, files in os.walk(BASE_DIR):
    for f in files:
        if f.endswith(".html"):
            html_files.append(os.path.join(root, f))

# regex for canonical
canon_regex = re.compile(r'<link\s+rel=["\']canonical["\'][^>]*>', re.IGNORECASE)
# regex for robots
robots_regex = re.compile(r'<meta\s+name=["\']robots["\'][^>]*>', re.IGNORECASE)

# Domains to replace in href
domains_to_replace = [
    "http://ottocean.sbs",
    "http://www.ottocean.sbs",
    "https://www.ottocean.sbs"
]

sitemap_urls = []

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    orig_content = content
    
    # 1. Remove NOINDEX and add clean index, follow
    content = robots_regex.sub('', content)
    # Insert new robots tag in head
    if '<head>' in content:
        content = content.replace('<head>', '<head>\n    <meta name="robots" content="index, follow">', 1)
    
    # 2. Fix Canonical Tags
    rel_path = os.path.relpath(filepath, BASE_DIR).replace('\\', '/')
    if rel_path == 'index.html':
        canonical_url = "https://ottocean.sbs/"
    else:
        canonical_url = f"https://ottocean.sbs/{rel_path}"
    
    canon_tag = f'<link rel="canonical" href="{canonical_url}">'
    if canon_regex.search(content):
        content = canon_regex.sub(canon_tag, content)
    else:
        if '</head>' in content:
            content = content.replace('</head>', f'    {canon_tag}\n</head>', 1)
            
    # Keep track for sitemap
    sitemap_urls.append(canonical_url)

    # 3. Fix Redirects & Links in hrefs
    def process_a_tag(match):
        a_tag_content = match.group(0)
        
        def process_href(href_match):
            href_val = href_match.group(1)
            new_href = href_val
            
            for d in domains_to_replace:
                if new_href.startswith(d):
                    new_href = "https://ottocean.sbs" + new_href[len(d):]
            
            # If it's a relative path like "blog.html" or "/blog.html"
            if not new_href.startswith("http") and not new_href.startswith("mailto:") and not new_href.startswith("tel:") and not new_href.startswith("#"):
                if new_href.startswith("/"):
                    new_href = f"https://ottocean.sbs{new_href}"
                else:
                    dir_part = os.path.dirname(rel_path)
                    if dir_part and dir_part != ".":
                        new_href = f"https://ottocean.sbs/{dir_part}/{new_href}"
                    else:
                        new_href = f"https://ottocean.sbs/{new_href}"

            if new_href.startswith("https://ottocean.sbs"):
                # Clean up index.html from URLs
                if new_href.endswith("index.html"):
                    new_href = new_href[:-10]
                    
                # Clean up trailing slashes
                if new_href.endswith("/") and new_href != "https://ottocean.sbs/":
                    new_href = new_href.rstrip("/")
            
            return f'href="{new_href}"'
            
        new_a_tag = re.sub(r'href=["\']([^"\']+)["\']', process_href, a_tag_content, flags=re.IGNORECASE)
        return new_a_tag

    content = re.sub(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>', process_a_tag, content, flags=re.IGNORECASE)
    
    if content != orig_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

# 4. Generate Sitemap
sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in sorted(sitemap_urls):
    sitemap_content += f'  <url>\n    <loc>{url}</loc>\n  </url>\n'
sitemap_content += '</urlset>\n'

with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
    f.write(sitemap_content)

print("SEO fixes applied successfully.")
