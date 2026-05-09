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

for fpath in html_files:
    fname = os.path.basename(fpath)
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        continue
        
    original = content
    content = fix_css(content)
    
    if fname in image_mapping:
        # Update the main featured image in the blog post
        # usually has class="article-featured-img", "post-hero-img", "article-hero-image"
        # or it is just the first image
        new_img = image_mapping[fname]
        
        # We find the first <img> and replace its src. Wait, what if there's a logo in the header?
        # Actually, let's replace any img src that has img/ or ../img/ (that isn't the favicon)
        # But maybe safer to find the img inside <article> or <main> or the first img after <header>
        
        # find the <img ...> tag containing class="post-hero-img" or "article-featured-img" or "article-hero-image"
        pattern = r'(<img\s+[^>]*src=")[^"]+("[^>]*>)'
        def replacer(match):
            tag = match.group(0)
            # don't replace if it's not a featured image
            if 'class=' in tag and ('hero' in tag or 'featured' in tag or 'thumb' in tag):
                # replace src
                new_tag = re.sub(r'src="[^"]+"', f'src="{new_img}"', tag)
                # ensure object-fit: cover and aspect-ratio: 16/9
                if 'style=' in new_tag:
                    if 'aspect-ratio' not in new_tag:
                        new_tag = re.sub(r'style="([^"]+)"', r'style="\1; aspect-ratio: 16/9; object-fit: cover;"', new_tag)
                else:
                    new_tag = new_tag.replace('>', ' style="aspect-ratio: 16/9; object-fit: cover;">')
                return new_tag
            # if we didn't match the specific class, see if it is just an img inside <article> or <div class="post-hero"> or similar.
            # actually we can just replace the first img that points to an image file that is NOT logo or favicon
            if ('logo' not in tag.lower() and 'favicon' not in tag.lower()):
                new_tag = re.sub(r'src="[^"]+"', f'src="{new_img}"', tag)
                if 'style=' in new_tag:
                    if 'aspect-ratio' not in new_tag:
                        new_tag = re.sub(r'style="([^"]+)"', r'style="\1; aspect-ratio: 16/9; object-fit: cover;"', new_tag)
                else:
                    new_tag = new_tag.replace('>', ' style="aspect-ratio: 16/9; object-fit: cover;">')
                # let's just return new_tag for the first one only?
                return new_tag
            return tag
        
        # Just replace the first matching img that isn't the logo
        content = re.sub(r'<img\s+[^>]*src="[^"]+"[^>]*>', replacer, content, count=1)
        
    if original != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {fname}")

print("Done")
