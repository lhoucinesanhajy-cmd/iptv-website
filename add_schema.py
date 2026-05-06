import os
import re
import json

base_dir = r'c:\Users\admin\Desktop\iptv-website'

def update_faq_schema(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    faq_items = re.findall(r'<label class="faq-question"[^>]*>\s*<span>(.*?)</span>.*?</label>\s*<div class="faq-answer">\s*<p>(.*?)</p>', content, re.DOTALL)
    
    if not faq_items:
        print(f"No FAQ items found in {filepath}")
        return

    mainEntity = []
    for q, a in faq_items:
        q = q.strip()
        a = a.strip()
        mainEntity.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": mainEntity
    }
    
    schema_json = json.dumps(faq_schema, indent=4)
    # properly indent the JSON inside the script
    indented_json = '\n'.join(['    ' + line for line in schema_json.split('\n')])
    script_tag = f'<!-- FAQ Schema -->\n    <script type="application/ld+json">\n{indented_json}\n    </script>\n</head>'
    
    # insert before </head>
    if '</head>' in content:
        # Check if FAQPage schema already exists
        if '"@type": "FAQPage"' not in content:
            content = content.replace('</head>', script_tag)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated FAQ in {filepath}")
        else:
            print(f"FAQ Schema already exists in {filepath}")
    else:
        print(f"No </head> found in {filepath}")

def update_blog_schema(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Headline (from <h1> inside the article or <title>)
    title_match = re.search(r'<title>(.*?)</title>', content)
    headline = title_match.group(1).replace(' — OttOcean IPTV', '').strip() if title_match else ""

    h1_match = re.search(r'<h1>(.*?)</h1>', content)
    if h1_match:
        headline = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()

    # Extract Date Published
    # e.g., <span class="article-meta-date"><i class="fa-regular fa-calendar"></i> May 15, 2026</span>
    date_match = re.search(r'<span class="article-meta-date">.*?</i>(.*?)</span>', content)
    date_pub = date_match.group(1).strip() if date_match else "May 1, 2026"

    # Extract Image URL
    # e.g., <img src="https://images.unsplash.com/..." class="article-hero-img" ...>
    img_match = re.search(r'<img src="([^"]+)"[^>]*class="article-hero-img"', content)
    if not img_match:
        img_match = re.search(r'<img[^>]*src="([^"]+)"', content)
    img_url = img_match.group(1) if img_match else "https://ottocean.sbs/favicon.png"

    blog_schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": headline,
        "author": {
            "@type": "Organization",
            "name": "OttOcean IPTV"
        },
        "datePublished": date_pub,
        "image": img_url
    }
    
    schema_json = json.dumps(blog_schema, indent=4)
    indented_json = '\n'.join(['    ' + line for line in schema_json.split('\n')])
    script_tag = f'<!-- Article Schema -->\n    <script type="application/ld+json">\n{indented_json}\n    </script>\n</head>'

    if '</head>' in content:
        if '"@type": "BlogPosting"' not in content:
            content = content.replace('</head>', script_tag)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated Blog Schema in {filepath}")
        else:
            print(f"Blog Schema already exists in {filepath}")

# Update FAQs
update_faq_schema(os.path.join(base_dir, 'index.html'))
update_faq_schema(os.path.join(base_dir, 'faq.html'))

# Update Blogs
blog_files = ['blog-post-1.html', 'blog-post-2.html', 'blog-post-3.html', 'blog-post-4.html', 'firestick-guide.html']
for b in blog_files:
    update_blog_schema(os.path.join(base_dir, b))
