import os
import re

html_files = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or '.git' in root: continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

def fix_css(content):
    if '.blog-card-thumb {' in content:
        content = re.sub(r'height:\s*200px;', r'aspect-ratio: 16/9;', content)
    return content

image_mapping = {
    'blog-post-14': 'img/champions-unique.jpg',
    'blog-post-13': 'img/nba-unique.jpg',
    'blog-post-12': 'img/australia-unique.jpg',
    'blog-post-11': 'img/champions-2-unique.jpg',
    'blog-post-10': 'img/isp-throttling-shield-unique.jpg',
    'blog-post-9': 'img/apple-tv-unique.jpg',
    'blog-post-8': 'img/ufc-premier-league-unique.jpg',
    'blog-post-1': 'img/network-security-unique.jpg',
    'blog-post-2': 'img/eliminate-throttling-unique.jpg',
    'blog-post-3': 'img/solve-throttling-2026-unique.jpg',
    'blog-post-4': 'img/hardware-software-unique.jpg',
    'blog-post-5': 'img/tivimate-smarters-unique.jpg',
    'blog-post-6': 'img/vpn-iptv-unique.jpg',
    'blog-post-7': 'img/firestick-setup-unique.jpg',
}

# we need to replace images inside blog.html
for fpath in html_files:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        continue
    
    original = content
    content = fix_css(content)
    
    # if it's blog.html, we can use the IDs to replace specific img src
    if fpath.endswith('blog.html'):
        for post_id, new_img in image_mapping.items():
            # regex to find <article class="blog-card" id="post_id">... <img src="..."
            pattern = r'(id="' + post_id + r'".*?<img src=")([^"]+)(")'
            content = re.sub(pattern, r'\g<1>' + new_img + r'\g<3>', content, flags=re.DOTALL)
            
    # For individual files, we can just replace the hero image or any img with class blog-card-thumb img or similar.
    # usually inside the article, they might have <img src="img/...">
    # Actually let's just do a specific replacement based on the filename
    fname = os.path.basename(fpath)
    if fname == 'watch-champions-league-final-2026.html':
        content = re.sub(r'<img src="([^"]+champions-league[^"]+)"', r'<img src="../img/champions-unique.jpg"', content)
        content = re.sub(r'<img src="../img/champions-unique.jpg" alt="([^"]+)" class="post-hero-img"', r'<img src="../img/champions-unique.jpg" alt="\g<1>" class="post-hero-img" style="aspect-ratio: 16/9; object-fit: cover;"', content)
    elif fname == 'best-iptv-nba-playoffs-2026.html':
        content = re.sub(r'<img src="([^"]+nba-playoffs[^"]+)"', r'<img src="../img/nba-unique.jpg"', content)
    elif fname == 'best-iptv-providers-australia-2026.html':
        content = re.sub(r'<img src="([^"]+australia[^"]+)"', r'<img src="../img/australia-unique.jpg"', content)
    elif fname == 'watch-champions-league-final-2026-4k.html':
        content = re.sub(r'<img src="([^"]+champions-league[^"]+)"', r'<img src="../img/champions-2-unique.jpg"', content)
    elif fname == 'why-is-my-iptv-blocked-isp-throttling.html':
        content = re.sub(r'<img src="([^"]+isp-throttling[^"]+)"', r'<img src="../img/isp-throttling-shield-unique.jpg"', content)
    elif fname == 'setup-iptv-apple-tv-4k.html':
        content = re.sub(r'<img src="([^"]+apple-tv[^"]+)"', r'<img src="img/apple-tv-unique.jpg"', content)
    elif fname == 'watch-ufc-premier-league-no-freezing.html':
        content = re.sub(r'<img src="([^"]+firestick-guide[^"]+)"', r'<img src="img/ufc-premier-league-unique.jpg"', content)
    elif fname == 'firestick-guide.html':
        content = re.sub(r'<img src="([^"]+firestick-guide[^"]+)"', r'<img src="img/firestick-setup-unique.jpg"', content)
    
    # Also enforce CSS fix directly in the html files if they contain .blog-card-thumb
    if original != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {fpath}")

print("Done")
