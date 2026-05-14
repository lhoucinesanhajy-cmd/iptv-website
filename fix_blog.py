import re

with open('blog.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. LCP FIX: First image fetchpriority="high", no loading attribute
content = re.sub(
    r'(<img src="https://i.ibb.co/7dFpH3yc/Chat-GPT-Image-May-14-2026-02-46-52-AM.png"[^>]+?)loading="eager"\s*([^>]*>)',
    r'\1\2',
    content
)
content = re.sub(
    r'(<img src="https://i.ibb.co/7dFpH3yc/Chat-GPT-Image-May-14-2026-02-46-52-AM.png"[^>]+?)loading="lazy"\s*([^>]*>)',
    r'\1\2',
    content
)

if 'fetchpriority="high"' not in content[:2500]:
    content = re.sub(
        r'(<img src="https://i.ibb.co/7dFpH3yc/Chat-GPT-Image-May-14-2026-02-46-52-AM.png"[^>]*?)>',
        r'\1 fetchpriority="high">',
        content
    )

# Clean up duplicate spaces or multiple fetchpriority
content = content.replace(' fetchpriority="high" fetchpriority="high"', ' fetchpriority="high"')
content = content.replace('  ', ' ')

# 2. CLS FIX: Reserve space for the blog-grid container
if '.blog-grid {' in content and 'min-height: 800px;' not in content:
    content = content.replace('.blog-grid {', '.blog-grid {\n            min-height: 800px;')

# 3. DOM OPTIMIZATION: Simplify the HTML structure of the blog cards
# Find <article class="blog-card" [id="..."]> <a href="..." style="..."> ... </a> </article>
# Replace with <a href="..." class="blog-card" [id="..."] style="..."> ... </a>
def replace_article(match):
    article_tag = match.group(1)
    a_tag = match.group(2)
    inner_content = match.group(3)
    
    id_match = re.search(r'id="([^"]+)"', article_tag)
    id_str = f' id="{id_match.group(1)}"' if id_match else ''
    
    href_match = re.search(r'href="([^"]+)"', a_tag)
    href_str = f' href="{href_match.group(1)}"' if href_match else ''
    
    style_match = re.search(r'style="([^"]+)"', a_tag)
    style_str = f' style="{style_match.group(1)}"' if style_match else ''
    
    return f'<a class="blog-card"{id_str}{href_str}{style_str}>\n{inner_content}\n        </a>'

pattern = re.compile(r'(<article class="blog-card"[^>]*>)\s*(<a[^>]*>)(.*?)\s*</a>\s*</article>', re.DOTALL)
content = pattern.sub(replace_article, content)

if 'display: block;' not in content.split('.blog-card {')[1][:100]:
    content = content.replace('.blog-card {', '.blog-card {\n            display: block;\n            text-decoration: none;')

# 4. RENDER BLOCKING: Move fonts and FontAwesome to bottom, move non-critical CSS to bottom
fonts_link = r'<link href="https://fonts.googleapis.com/css2[^>]+rel="stylesheet">'
fa_link = r'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css"[^>]+>'

fonts_match = re.search(fonts_link, content)
fa_match = re.search(fa_link, content)

if fonts_match:
    content = content.replace(fonts_match.group(0), '')
if fa_match:
    content = content.replace(fa_match.group(0), '')

# Extract non-critical CSS
rules_to_extract = [
    r'\s*\.blog-card:hover\s*\{[^}]+\}',
    r'\s*\.blog-card:hover\s+\.blog-card-thumb\s+img\s*\{[^}]+\}',
    r'\s*\.blog-tag--tips\s*\{[^}]+\}',
    r'\s*\.blog-tag--news\s*\{[^}]+\}',
    r'\s*\.blog-tag--review\s*\{[^}]+\}',
    r'\s*\.blog-coming-soon\s*\{[^}]+\}',
    r'\s*\.blog-coming-soon\s+\.soon-icon\s*\{[^}]+\}',
    r'\s*\.blog-coming-soon\s+h2\s*\{[^}]+\}',
    r'\s*\.blog-coming-soon\s+p\s*\{[^}]+\}',
    r'\s*\/\*\s*----\s*Pagination styles\s*----\s*\*\/\s*\.pagination\s*\{[^}]+\}\s*\.pagination\s+a\s*\{[^}]+\}\s*\.pagination\s+a:hover,\s*\.pagination\s+a\.active\s*\{[^}]+\}'
]

extracted_css = ""
for rule in rules_to_extract:
    matches = list(re.finditer(rule, content))
    for match in matches:
        extracted_css += match.group(0) + "\n"
        content = content.replace(match.group(0), '')

bottom_injections = f"""
    <!-- Deferred CSS & Fonts -->
    {fonts_match.group(0) if fonts_match else ''}
    {fa_match.group(0) if fa_match else ''}
    <style>
{extracted_css}
    </style>
"""

if '<!-- Deferred CSS & Fonts -->' not in content:
    content = content.replace('</body>', f'{bottom_injections}\n</body>')

with open('blog.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Blog optimization applied successfully.")
