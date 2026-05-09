import os
import re

html_files = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or '.git' in root: continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

image_mapping = {
    'watch-champions-league-final-2026.html': '../img/champions-unique.jpg',
    'best-iptv-nba-playoffs-2026.html': '../img/nba-unique.jpg',
    'best-iptv-providers-australia-2026.html': '../img/australia-unique.jpg',
    'watch-champions-league-final-2026-4k.html': '../img/champions-2-unique.jpg',
    'why-is-my-iptv-blocked-isp-throttling.html': '../img/isp-throttling-shield-unique.jpg',
    'setup-iptv-apple-tv-4k.html': 'img/apple-tv-unique.jpg',
    'watch-ufc-premier-league-no-freezing.html': 'img/ufc-premier-league-unique.jpg',
    'blog-post-1.html': 'img/network-security-unique.jpg',
    'blog-post-2.html': 'img/eliminate-throttling-unique.jpg',
    'blog-post-3.html': 'img/solve-throttling-2026-unique.jpg',
    'blog-post-4.html': 'img/hardware-software-unique.jpg',
    'blog-post-5.html': 'img/tivimate-smarters-unique.jpg',
    'blog-post-6.html': 'img/vpn-iptv-unique.jpg',
    'firestick-guide.html': 'img/firestick-setup-unique.jpg',
}

def process_file(fpath, fname):
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return
        
    original = content
    
    if fname in image_mapping:
        new_img = image_mapping[fname]
        
        replaced = False
        def replacer(match):
            nonlocal replaced
            tag = match.group(0)
            if replaced:
                return tag
                
            if 'class=' in tag and ('hero' in tag or 'featured' in tag or 'thumb' in tag):
                new_tag = re.sub(r'src="[^"]+"', f'src="{new_img}"', tag)
                if 'style=' in new_tag:
                    if 'aspect-ratio' not in new_tag:
                        new_tag = re.sub(r'style="([^"]+)"', r'style="\1; aspect-ratio: 16/9; object-fit: cover;"', new_tag)
                else:
                    new_tag = new_tag.replace('>', ' style="aspect-ratio: 16/9; object-fit: cover;">')
                replaced = True
                return new_tag
            elif 'logo' not in tag.lower() and 'favicon' not in tag.lower():
                new_tag = re.sub(r'src="[^"]+"', f'src="{new_img}"', tag)
                if 'style=' in new_tag:
                    if 'aspect-ratio' not in new_tag:
                        new_tag = re.sub(r'style="([^"]+)"', r'style="\1; aspect-ratio: 16/9; object-fit: cover;"', new_tag)
                else:
                    new_tag = new_tag.replace('>', ' style="aspect-ratio: 16/9; object-fit: cover;">')
                replaced = True
                return new_tag
            return tag
            
        content = re.sub(r'<img\s+[^>]*src="[^"]+"[^>]*>', replacer, content)
        
    if original != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {fname}")

for fpath in html_files:
    process_file(fpath, os.path.basename(fpath))

print("Done")
