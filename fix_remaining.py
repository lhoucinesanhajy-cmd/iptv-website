import os
import re

files_to_update = {
    'blog/best-iptv-nba-playoffs-2026.html': '../img/nba-unique.jpg',
    'blog/best-iptv-providers-australia-2026.html': '../img/australia-unique.jpg',
    'blog/why-is-my-iptv-blocked-isp-throttling.html': '../img/isp-throttling-shield-unique.jpg',
    'setup-iptv-apple-tv-4k.html': 'img/apple-tv-unique.jpg',
    'watch-ufc-premier-league-no-freezing.html': 'img/ufc-premier-league-unique.jpg',
    'firestick-guide.html': 'img/firestick-setup-unique.jpg',
    'blog/watch-champions-league-final-2026-4k.html': '../img/champions-2-unique.jpg',
    'blog-post-1.html': 'img/network-security-unique.jpg'
}

def update_file(fpath, new_img):
    if not os.path.exists(fpath): return
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    replaced = False
    def replacer(match):
        nonlocal replaced
        tag = match.group(0)
        if replaced: return tag
        if 'logo' not in tag.lower() and 'favicon' not in tag.lower():
            new_tag = re.sub(r'src="[^"]+"', f'src="{new_img}"', tag)
            if 'style=' in new_tag:
                if 'aspect-ratio' not in new_tag:
                    new_tag = re.sub(r'style="([^"]+)"', r'style="\1; aspect-ratio: 16/9; object-fit: cover;"', new_tag)
            else:
                new_tag = new_tag.replace('>', ' style="aspect-ratio: 16/9; object-fit: cover;">')
            replaced = True
            return new_tag
        return tag
        
    new_content = re.sub(r'<img\s+[^>]*src="[^"]+"[^>]*>', replacer, content)
    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {fpath}")

for fpath, new_img in files_to_update.items():
    update_file(fpath, new_img)

