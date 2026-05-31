import os
import re

template_path = r"c:\Users\admin\Desktop\iptv-website\blog-post-1.html"
article_path = r"c:\Users\admin\Desktop\iptv-website\best-iptv-uk-2026.html"

with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

header_split = template.split('<div class="article-content">')
header = header_split[0] + '<div class="article-content">\n'

footer_split = template.split('</main>')
footer = '\n</main>' + footer_split[1]

# Modify header metadata for the new article
header = header.replace('<title>How to Secure Your Home Network for High-Speed Streaming - OttOcean IPTV</title>', '<title>Best IPTV Services in the UK for 2026 - OttOcean IPTV</title>')
header = header.replace('<meta name="description" content="OttOcean IPTV guide: Secure your home network for high-speed streaming with essential protection tips.">', '<meta name="description" content="Best IPTV Services in the UK for 2026: Ultimate Guide for Live Sports & Entertainment.">')
header = header.replace('<h1 class="article-title">How to Secure Your Home Network for High-Speed Streaming</h1>', '<h1 class="article-title">Best IPTV Services in the UK for 2026</h1>')
header = header.replace('<span class="article-tag">Security</span>', '<span class="article-tag">Guide</span>')
header = header.replace('May 1, 2026', 'May 31, 2026')
header = header.replace('5 min read', '10 min read')

with open(article_path, 'r', encoding='utf-8') as f:
    article_content = f.read()

# Remove the original h1 from article_content since we put it in the header
article_content = re.sub(r'<h1>.*?</h1>', '', article_content, flags=re.IGNORECASE | re.DOTALL)

with open(article_path, 'w', encoding='utf-8') as f:
    f.write(header + article_content + footer)

print("Wrapped article successfully.")
