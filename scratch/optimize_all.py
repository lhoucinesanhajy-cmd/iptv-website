"""
Final performance optimization script for blog.html and site-wide Clarity deferral.
1. Minifies blog.html: removes blank lines, comments, extra whitespace, inlines all CSS
2. Uses script.min.js instead of script.js
3. Defers Clarity tracking by 5 seconds on all pages
4. Converts local img/ JPG/PNG to WebP
"""
import re, os, glob

BASE = r"c:\Users\admin\Desktop\iptv-website"

# ============================================================
# STEP 1: Generate fully minified blog.html
# ============================================================
def minify_blog():
    src = os.path.join(BASE, "blog.html")
    with open(src, "r", encoding="utf-8") as f:
        html = f.read()

    # Remove all HTML comments (except IE conditionals)
    html = re.sub(r'<!--(?!\[if).*?-->', '', html, flags=re.DOTALL)

    # Remove blank lines and trim each line
    lines = html.split('\n')
    lines = [l.strip().replace('\r','') for l in lines]
    lines = [l for l in lines if l]  # remove empty lines
    html = '\n'.join(lines)

    # Collapse multiple newlines
    html = re.sub(r'\n{2,}', '\n', html)

    # Use script.min.js instead of script.js
    html = html.replace('src="script.js"', 'src="script.min.js"')

    # Minify inline <style> blocks - collapse whitespace inside them
    def minify_css_block(match):
        tag_open = match.group(1)
        css = match.group(2)
        tag_close = match.group(3)
        # Remove CSS comments
        css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
        # Collapse whitespace
        css = re.sub(r'\s+', ' ', css)
        # Remove spaces around CSS punctuation
        css = re.sub(r'\s*{\s*', '{', css)
        css = re.sub(r'\s*}\s*', '}', css)
        css = re.sub(r'\s*;\s*', ';', css)
        css = re.sub(r'\s*:\s*', ':', css)
        css = re.sub(r'\s*,\s*', ',', css)
        css = css.strip()
        return tag_open + css + tag_close

    html = re.sub(r'(<style[^>]*>)(.*?)(</style>)', minify_css_block, html, flags=re.DOTALL)

    # Minify JSON-LD blocks - collapse whitespace
    def minify_jsonld(match):
        prefix = match.group(1)
        content = match.group(2)
        suffix = match.group(3)
        content = re.sub(r'\s+', ' ', content).strip()
        return prefix + content + suffix

    html = re.sub(
        r'(<script type="application/ld\+json">)(.*?)(</script>)',
        minify_jsonld, html, flags=re.DOTALL
    )

    # Final: collapse remaining multi-newlines and write
    html = re.sub(r'\n{2,}', '\n', html)

    with open(src, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] blog.html minified: {len(html)} bytes")

# ============================================================
# STEP 2: Defer Microsoft Clarity by 5 seconds on ALL pages
# ============================================================
CLARITY_PATTERN = re.compile(
    r'<!-- Microsoft Clarity -->\s*<script[^>]*>\s*\(function\s*\(.*?\)\s*\{.*?clarity.*?\}\)\(window,\s*document,\s*"clarity",\s*"script",\s*"(\w+)"\);\s*</script>',
    re.DOTALL
)

def make_deferred_clarity(tag_id):
    return f'<script>setTimeout(function(){{(function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y)}})(window,document,"clarity","script","{tag_id}")}},5000)</script>'

def defer_clarity_all():
    patterns = [
        os.path.join(BASE, "*.html"),
        os.path.join(BASE, "blog", "*.html"),
    ]
    count = 0
    for pat in patterns:
        for fpath in glob.glob(pat):
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            m = CLARITY_PATTERN.search(content)
            if m:
                tag_id = m.group(1)
                new_content = CLARITY_PATTERN.sub(make_deferred_clarity(tag_id), content)
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                count += 1
                print(f"  [DEFERRED] {os.path.basename(fpath)}")
    print(f"[OK] Clarity deferred on {count} files")

# ============================================================
# STEP 3: Convert local img/ files to WebP + update references
# ============================================================
def convert_images_to_webp():
    try:
        from PIL import Image
    except ImportError:
        print("[SKIP] Pillow not installed, skipping WebP conversion")
        return

    img_dir = os.path.join(BASE, "img")
    converted = []
    for ext in ("*.jpg", "*.jpeg", "*.png"):
        for fpath in glob.glob(os.path.join(img_dir, ext)):
            webp_path = os.path.splitext(fpath)[0] + ".webp"
            if not os.path.exists(webp_path):
                img = Image.open(fpath)
                img.save(webp_path, "WEBP", quality=75, method=6)
                print(f"  [WEBP] {os.path.basename(fpath)} -> {os.path.basename(webp_path)}")
            converted.append((
                "img/" + os.path.basename(fpath),
                "img/" + os.path.basename(webp_path)
            ))

    # Update references in all HTML files
    if converted:
        for pat in [os.path.join(BASE, "*.html"), os.path.join(BASE, "blog", "*.html")]:
            for fpath in glob.glob(pat):
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                changed = False
                for old, new in converted:
                    if old in content:
                        content = content.replace(old, new)
                        changed = True
                if changed:
                    with open(fpath, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"  [REFS] Updated {os.path.basename(fpath)}")
    print(f"[OK] Converted {len(converted)} images to WebP")

# ============================================================
# STEP 4: Also minify blog-page-2.html the same way
# ============================================================
def minify_html_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    html = re.sub(r'<!--(?!\[if).*?-->', '', html, flags=re.DOTALL)
    lines = html.split('\n')
    lines = [l.strip().replace('\r','') for l in lines]
    lines = [l for l in lines if l]
    html = '\n'.join(lines)
    html = re.sub(r'\n{2,}', '\n', html)
    html = html.replace('src="script.js"', 'src="script.min.js"')
    def minify_css_block(match):
        css = match.group(2)
        css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
        css = re.sub(r'\s+', ' ', css)
        for ch in ['{','}',';',':',',']:
            css = re.sub(r'\s*\\' + ch + r'\s*' if ch in '{}' else r'\s*[' + re.escape(ch) + r']\s*', ch, css)
        css = re.sub(r'\s*{\s*', '{', css)
        css = re.sub(r'\s*}\s*', '}', css)
        css = re.sub(r'\s*;\s*', ';', css)
        css = re.sub(r'\s*:\s*', ':', css)
        css = re.sub(r'\s*,\s*', ',', css)
        return match.group(1) + css.strip() + match.group(3)
    html = re.sub(r'(<style[^>]*>)(.*?)(</style>)', minify_css_block, html, flags=re.DOTALL)
    def minify_jsonld(match):
        content = re.sub(r'\s+', ' ', match.group(2)).strip()
        return match.group(1) + content + match.group(3)
    html = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', minify_jsonld, html, flags=re.DOTALL)
    html = re.sub(r'\n{2,}', '\n', html)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] Minified {os.path.basename(filepath)}: {len(html)} bytes")

# ============================================================
# RUN ALL
# ============================================================
if __name__ == "__main__":
    print("=== STEP 1: Minify blog.html ===")
    minify_blog()

    print("\n=== STEP 2: Minify blog-page-2.html ===")
    p2 = os.path.join(BASE, "blog-page-2.html")
    if os.path.exists(p2):
        minify_html_file(p2)

    print("\n=== STEP 3: Defer Clarity (5s delay) ===")
    defer_clarity_all()

    print("\n=== STEP 4: Convert images to WebP ===")
    convert_images_to_webp()

    print("\n=== ALL DONE ===")
