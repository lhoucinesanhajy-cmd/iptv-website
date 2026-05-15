"""
Global PageSpeed 90+ optimization script for index.html, pricing.html, blog.html, faq.html
Applies: critical CSS inlining, CSS deferral, defer/async scripts, font-display:swap,
         WebP image references, lazy-loading, fetchpriority=high on LCP, DOM minification
"""
import re, os

BASE = r"c:\Users\admin\Desktop\iptv-website"

# ─── CRITICAL CSS blocks (above-the-fold only) ──────────────────────────────
CRITICAL_COMMON = """*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;max-width:100%}html{overflow-x:hidden;-webkit-text-size-adjust:100%}body{font-family:'Inter',system-ui,sans-serif;background:#0f051c;color:#e0d8f0;line-height:1.6;overflow-x:hidden;width:100%;max-width:100vw}a{text-decoration:none;color:inherit}ul{list-style:none}header{position:fixed;top:0;left:0;width:100%;z-index:1000;background:transparent;transition:background .4s,box-shadow .4s}header.scrolled{background:rgba(15,5,28,.92);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);box-shadow:0 1px 0 rgba(255,255,255,.05)}.nav-container{max-width:1200px;margin:0 auto;padding:0 40px;height:68px;display:flex;align-items:center;justify-content:space-between;gap:32px}.logo{font-size:1.5rem;font-weight:800;background:linear-gradient(135deg,#a855f7,#6366f1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:-.5px;white-space:nowrap;flex-shrink:0}.nav-links{display:flex;align-items:center;gap:6px}.nav-link{position:relative;display:inline-block;padding:8px 14px;font-size:.9rem;font-weight:500;color:rgba(255,255,255,.75);border-radius:8px;transition:color .25s,background .25s}.nav-toggle{display:none;flex-direction:column;justify-content:center;align-items:center;gap:5px;width:40px;height:40px;background:transparent;border:1px solid rgba(255,255,255,.12);border-radius:8px;cursor:pointer;padding:0;flex-shrink:0}.nav-toggle span{display:block;width:20px;height:2px;background:#fff;border-radius:2px}.nav-trial-btn{display:inline-flex;align-items:center;padding:9px 22px;font-family:'Poppins',system-ui,sans-serif;font-size:.85rem;font-weight:700;color:#fff;background:linear-gradient(135deg,#a855f7 0%,#7c3aed 50%,#6366f1 100%);border-radius:50px;border:1.5px solid rgba(168,85,247,.55);white-space:nowrap;flex-shrink:0}@media(max-width:768px){.nav-container{padding:0 16px;height:62px}.nav-toggle{display:flex;z-index:1100;position:relative}.nav-links{position:fixed;top:62px;left:0;right:0;width:100vw;flex-direction:column;align-items:stretch;gap:0;background:rgba(15,5,28,.98);max-height:0;overflow:hidden;opacity:0;pointer-events:none;transition:max-height .35s,opacity .3s,padding .3s;z-index:1050}.nav-links.open{max-height:420px;opacity:1;pointer-events:auto}}"""

CRITICAL_INDEX = CRITICAL_COMMON + """#hero{min-height:100vh;background:#0f051c;display:flex;align-items:center;padding:0 40px;position:relative;overflow:hidden;width:100%;max-width:100vw}.hero-inner{max-width:1200px;width:100%;margin:0 auto;display:flex;align-items:center;gap:64px;padding:120px 0 80px}.hero-content{flex:1;min-width:0}.hero-badge{display:inline-block;padding:8px 18px;font-size:.78rem;font-weight:600;color:#a855f7;background:rgba(168,85,247,.1);border:1px solid rgba(168,85,247,.25);border-radius:50px;margin-bottom:28px;letter-spacing:.4px}.hero-content h1{font-family:'Poppins',system-ui,sans-serif;font-size:clamp(2.6rem,5vw,4rem);font-weight:900;line-height:1.08;letter-spacing:-1.5px;color:#fff;margin-bottom:8px}.hero-highlight{background:linear-gradient(135deg,#a855f7 0%,#6366f1 60%,#38bdf8 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}.hero-sub{font-size:1.08rem;color:rgba(224,216,240,.62);line-height:1.82;margin-top:20px;margin-bottom:36px;max-width:460px}.hero-buttons{display:flex;gap:14px;align-items:center;flex-wrap:wrap}.cta-btn{display:inline-block;padding:15px 38px;font-family:'Poppins',system-ui,sans-serif;font-size:.97rem;font-weight:700;color:#fff;background:linear-gradient(135deg,#a855f7,#6366f1);border:none;border-radius:12px;cursor:pointer;box-shadow:0 4px 24px rgba(168,85,247,.35)}.cta-btn-outline{display:inline-block;padding:15px 38px;font-size:.97rem;font-weight:600;color:rgba(255,255,255,.8);background:transparent;border:1px solid rgba(255,255,255,.15);border-radius:12px;cursor:pointer}.hero-visual{flex:1;min-width:0;position:relative;display:flex;justify-content:center;align-items:center}@media(max-width:768px){#hero{padding:0 20px}.hero-inner{flex-direction:column;gap:40px;padding:100px 0 60px}.hero-content h1{font-size:clamp(2rem,8vw,2.8rem)}}"""

CRITICAL_PAGE = CRITICAL_COMMON + """.page-hero{padding:140px 40px 80px;text-align:center;background:#0f051c;position:relative;overflow:hidden}.page-hero::before{content:"";position:absolute;width:700px;height:700px;background:radial-gradient(circle,rgba(168,85,247,.1) 0%,transparent 70%);top:-200px;left:50%;transform:translateX(-50%);border-radius:50%;pointer-events:none}.page-hero-inner{max-width:800px;margin:0 auto;position:relative;z-index:1}.page-hero-tag{display:inline-block;padding:7px 18px;font-size:.78rem;font-weight:600;color:#a855f7;background:rgba(168,85,247,.1);border:1px solid rgba(168,85,247,.25);border-radius:50px;margin-bottom:24px;letter-spacing:.5px}.page-hero h1{font-family:'Poppins',system-ui,sans-serif;font-size:clamp(2.2rem,4.5vw,3.4rem);font-weight:900;line-height:1.1;letter-spacing:-1px;color:#fff;margin-bottom:18px}.page-hero h1 span{background:linear-gradient(135deg,#a855f7 0%,#6366f1 60%,#38bdf8 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}.page-hero p{font-size:1.05rem;color:rgba(224,216,240,.6);line-height:1.8;max-width:580px;margin:0 auto}@media(max-width:768px){.page-hero{padding:110px 20px 60px}}"""

CRITICAL_BLOG = CRITICAL_PAGE + """.blog-card-thumb{width:100%;aspect-ratio:16/9;overflow:hidden;background:#0d0d1a;position:relative}.blog-card-thumb img{width:100%;height:100%;object-fit:cover;display:block}.blog-grid{max-width:1100px;margin:0 auto;padding:0 40px 80px;display:grid;grid-template-columns:repeat(3,1fr);gap:28px}@media(max-width:900px){.blog-grid{grid-template-columns:repeat(2,1fr)}}@media(max-width:600px){.blog-grid{grid-template-columns:1fr;padding:0 20px 60px}}.blog-card{display:block;text-decoration:none;background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.08);border-radius:18px;overflow:hidden}.blog-card-body{padding:22px 22px 24px}.blog-tag{display:inline-block;padding:4px 12px;border-radius:50px;font-size:.7rem;font-weight:700;letter-spacing:.4px;text-transform:uppercase;margin-bottom:12px}.blog-tag--guide{background:rgba(168,85,247,.15);color:#c084fc;border:1px solid rgba(168,85,247,.3)}.blog-card-title{font-family:'Poppins',sans-serif;font-size:1.05rem;font-weight:700;color:#fff;line-height:1.4;margin-bottom:10px}.blog-card-excerpt{font-size:.88rem;color:rgba(224,216,240,.55);line-height:1.7;margin-bottom:18px}.blog-card-meta{display:flex;align-items:center;justify-content:space-between;font-size:.75rem;color:rgba(224,216,240,.4)}"""

# Deferred CSS loader snippet
DEFER_CSS = """<link rel="preload" href="style.css" as="style" onload="this.onload=null;this.rel='stylesheet'"><noscript><link rel="stylesheet" href="style.css"></noscript>"""
DEFER_FA  = """<link rel="preload" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" as="style" onload="this.onload=null;this.rel='stylesheet'" crossorigin="anonymous" referrerpolicy="no-referrer"><noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer"></noscript>"""

# WA widget deferred (4s delay on non-interaction)
WA_DEFER_INIT = """<script>
(function(){var wa=document.querySelector('.floating-wa');if(wa){wa.style.display='none';var show=function(){if(wa.style.display==='none'){wa.style.display='flex';}};var t=setTimeout(show,4000);['scroll','touchstart','mousemove','keydown'].forEach(function(e){window.addEventListener(e,function h(){show();clearTimeout(t);window.removeEventListener(e,h);},{once:true,passive:true});});}})();
</script>"""

def minify_html(html):
    # Remove blank-only lines
    lines = [l for l in html.split('\n') if l.strip()]
    return '\n'.join(lines)

def remove_render_blockers(html):
    """Remove blocking CSS links and replace with deferred versions."""
    # Remove blocking style.css link
    html = re.sub(r'<link[^>]+rel=["\']stylesheet["\'][^>]+href=["\']style\.css["\'][^>]*>', '', html)
    html = re.sub(r'<link[^>]+href=["\']style\.css["\'][^>]+rel=["\']stylesheet["\'][^>]*>', '', html)
    # Remove blocking Font Awesome link
    html = re.sub(r'<link[^>]+font-awesome[^>]+rel=["\']stylesheet["\'][^>]*/>', '', html)
    html = re.sub(r'<link[^>]+rel=["\']stylesheet["\'][^>]+font-awesome[^>]*/>', '', html)
    # Add font-display:swap to Google Fonts URL
    html = html.replace(
        'family=Inter:wght@400;500;600;700;800&family=Poppins:wght@700;800;900&display=swap',
        'family=Inter:wght@400;500;600;700;800&family=Poppins:wght@700;800;900&display=swap'
    )
    # Ensure fonts have display=swap (already in URL) and are preloaded
    html = re.sub(
        r'(<link[^>]+fonts\.googleapis\.com/css2[^>]+)rel=["\']stylesheet["\']([^>]*>)',
        r'\1rel="preload" as="style" onload="this.onload=null;this.rel=\'stylesheet\'"\2<noscript><link\1rel="stylesheet"\2</noscript>',
        html
    )
    return html

def add_script_defer(html):
    """Add defer to all script tags that don't already have defer/async."""
    def replace_script(m):
        tag = m.group(0)
        if 'defer' in tag or 'async' in tag or 'type="application/ld+json"' in tag:
            return tag
        return tag.replace('<script ', '<script defer ')
    return re.sub(r'<script [^>]*src=[^>]*>', replace_script, html)

def process_images(html, is_lcp_first=True):
    """Add lazy loading to all images, fetchpriority=high to first."""
    first = [True]
    def replace_img(m):
        tag = m.group(0)
        # Skip if already has loading attribute
        if 'loading=' in tag:
            return tag
        # Convert .png/.jpg to .webp where local
        tag = re.sub(r'(src=["\'])([^"\']+/img/[^"\']+)\.(jpg|png)(["\'])', r'\1\2.webp\4', tag)
        tag = re.sub(r'(src=["\'])([^"\']+/images/[^"\']+)\.(png)(["\'])', r'\1\2.webp\4', tag)
        tag = re.sub(r'(src=["\'])(img/[^"\']+)\.(jpg|png)(["\'])', r'\1\2.webp\4', tag)
        tag = re.sub(r'(src=["\'])(images/[^"\']+)\.(png)(["\'])', r'\1\2.webp\4', tag)
        # Also favicon
        if 'logo.png' in tag:
            tag = tag.replace('logo.png', 'logo.webp')
        if is_lcp_first and first[0]:
            first[0] = False
            # LCP image - eager load + fetchpriority
            tag = tag.replace('<img ', '<img fetchpriority="high" decoding="async" ')
        else:
            tag = tag.replace('<img ', '<img loading="lazy" decoding="async" ')
        return tag
    return re.sub(r'<img [^>]*>', replace_img, html)

def fix_cls(html):
    """Add width/height to icon containers to fix CLS."""
    # nav-toggle spans have explicit size in CSS; floating-wa fix
    html = html.replace(
        'style="width: 35px; height: 35px;"',
        'width="35" height="35" style="width:35px;height:35px"'
    )
    return html

def build_head_index(orig_head):
    """Rebuild optimized <head> for index.html."""
    # Extract meta charset, viewport, title, description, keywords
    charset = re.search(r'<meta charset=[^>]+>', orig_head)
    gsc = re.search(r'<meta name="google-site-verification"[^>]+>', orig_head)
    viewport = '<meta name="viewport" content="width=device-width,initial-scale=1">'
    title = re.search(r'<title>[^<]+</title>', orig_head)
    desc = re.search(r'<meta name="description"[^>]+>', orig_head)
    keywords = re.search(r'<meta name="keywords"[^>\n]*([\s\S]*?)>', orig_head)
    
    # Extract all schema/ld+json blocks
    schemas = re.findall(r'<script type="application/ld\+json">[\s\S]*?</script>', orig_head)
    schemas_min = []
    for s in schemas:
        inner = re.search(r'<script[^>]*>([\s\S]*?)</script>', s)
        if inner:
            j = re.sub(r'\s+', ' ', inner.group(1)).strip()
            schemas_min.append(f'<script type="application/ld+json">{j}</script>')
    
    # OG/twitter/canonical/sitemap/etc
    og = re.findall(r'<meta property="og:[^>]+>', orig_head)
    tw = re.findall(r'<meta name="twitter:[^>]+>', orig_head)
    canonical = re.search(r'<link rel="canonical"[^>]+>', orig_head)
    icon = re.search(r'<link rel="icon"[^>]+>', orig_head)
    atouch = re.search(r'<link rel="apple-touch-icon"[^>]+>', orig_head)
    manifest = re.search(r'<link rel="manifest"[^>]+>', orig_head)
    sitemap = re.search(r'<link rel="sitemap"[^>]+>', orig_head)
    geo_r = re.search(r'<meta name="geo\.region"[^>]+>', orig_head)
    geo_p = re.search(r'<meta name="geo\.placename"[^>]+>', orig_head)
    
    parts = ['<head>']
    if charset: parts.append(charset.group(0))
    if gsc: parts.append(gsc.group(0))
    parts.append(viewport)
    if title: parts.append(title.group(0))
    if desc: parts.append(desc.group(0))
    if keywords:
        kw_content = re.search(r'content="([^"]+)"', keywords.group(0))
        if kw_content:
            parts.append(f'<meta name="keywords" content="{kw_content.group(1)}">')
    # Preconnects
    parts.append('<link rel="preconnect" href="https://fonts.googleapis.com">')
    parts.append('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    # Preload deferred font
    parts.append('<link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@700;800;900&display=swap" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">')
    parts.append('<noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@700;800;900&display=swap" rel="stylesheet"></noscript>')
    # Critical CSS inline
    parts.append(f'<style>{CRITICAL_INDEX}</style>')
    # Deferred full CSS
    parts.append(DEFER_CSS)
    parts.append(DEFER_FA)
    # OG/twitter/canonical/etc
    for tag in og: parts.append(tag)
    for tag in tw: parts.append(tag)
    if canonical: parts.append(canonical.group(0))
    if icon: parts.append(icon.group(0))
    if atouch: parts.append(atouch.group(0))
    if manifest: parts.append(manifest.group(0))
    if sitemap: parts.append(sitemap.group(0))
    if geo_r: parts.append(geo_r.group(0))
    if geo_p: parts.append(geo_p.group(0))
    for s in schemas_min: parts.append(s)
    parts.append('</head>')
    return '\n'.join(parts)

def build_head_page(orig_head, critical_css, page_lcp_preload=None):
    """Rebuild optimized <head> for pricing/faq/blog."""
    charset = re.search(r'<meta charset=[^>]+>', orig_head)
    gsc = re.search(r'<meta name="google-site-verification"[^>]+>', orig_head)
    viewport = '<meta name="viewport" content="width=device-width,initial-scale=1">'
    title = re.search(r'<title>[^<]+</title>', orig_head)
    desc = re.search(r'<meta name="description"[^>]+>', orig_head)
    schemas = re.findall(r'<script type="application/ld\+json">[\s\S]*?</script>', orig_head)
    schemas_min = []
    for s in schemas:
        inner = re.search(r'<script[^>]*>([\s\S]*?)</script>', s)
        if inner:
            j = re.sub(r'\s+', ' ', inner.group(1)).strip()
            schemas_min.append(f'<script type="application/ld+json">{j}</script>')
    og = re.findall(r'<meta property="og:[^>]+>', orig_head)
    tw = re.findall(r'<meta name="twitter:[^>]+>', orig_head)
    canonical = re.search(r'<link rel="canonical"[^>]+>', orig_head)
    icon = re.search(r'<link rel="icon"[^>]+>', orig_head)
    atouch = re.search(r'<link rel="apple-touch-icon"[^>]+>', orig_head)
    manifest = re.search(r'<link rel="manifest"[^>]+>', orig_head)
    sitemap = re.search(r'<link rel="sitemap"[^>]+>', orig_head)
    geo_r = re.search(r'<meta name="geo\.region"[^>]+>', orig_head)
    geo_p = re.search(r'<meta name="geo\.placename"[^>]+>', orig_head)
    next_link = re.search(r'<link rel="next"[^>]+>', orig_head)
    
    parts = ['<head>']
    if charset: parts.append(charset.group(0))
    if gsc: parts.append(gsc.group(0))
    parts.append(viewport)
    if title: parts.append(title.group(0))
    if desc: parts.append(desc.group(0))
    parts.append('<link rel="preconnect" href="https://fonts.googleapis.com">')
    parts.append('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    if page_lcp_preload:
        parts.append(f'<link rel="preload" as="image" href="{page_lcp_preload}" fetchpriority="high">')
    parts.append('<link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@700;800;900&display=swap" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">')
    parts.append('<noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@700;800;900&display=swap" rel="stylesheet"></noscript>')
    parts.append(f'<style>{critical_css}</style>')
    parts.append(DEFER_CSS)
    parts.append(DEFER_FA)
    for tag in og: parts.append(tag)
    for tag in tw: parts.append(tag)
    if canonical: parts.append(canonical.group(0))
    if icon: parts.append(icon.group(0))
    if atouch: parts.append(atouch.group(0))
    if manifest: parts.append(manifest.group(0))
    if sitemap: parts.append(sitemap.group(0))
    if next_link: parts.append(next_link.group(0))
    if geo_r: parts.append(geo_r.group(0))
    if geo_p: parts.append(geo_p.group(0))
    for s in schemas_min: parts.append(s)
    parts.append('</head>')
    return '\n'.join(parts)

def optimize_body(html_body):
    """Apply all body optimizations."""
    # Ensure script.js uses defer
    html_body = re.sub(r'<script src="script\.js">', '<script src="script.min.js" defer>', html_body)
    html_body = re.sub(r'<script src="script\.js" defer>', '<script src="script.min.js" defer>', html_body)
    html_body = re.sub(r'<script src="\.\./script\.js">', '<script src="../script.min.js" defer>', html_body)
    # Fix floating WA widget display (it's rendered inline; move to deferred)
    # Process images
    html_body = process_images(html_body)
    # Fix CLS on SVG icons
    html_body = fix_cls(html_body)
    # Add WA defer init before </body>
    html_body = html_body.replace('</body>', WA_DEFER_INIT + '\n</body>')
    return html_body

def optimize_file(path, critical_css=None, lcp_preload=None, is_index=False):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Split head and body
    head_match = re.search(r'<head>([\s\S]*?)</head>', html, re.IGNORECASE)
    body_match = re.search(r'<body>([\s\S]*)</body>', html, re.IGNORECASE)
    
    if not head_match or not body_match:
        print(f"WARN: could not find head/body in {path}")
        return
    
    orig_head = head_match.group(1)
    orig_body = body_match.group(1)
    
    if is_index:
        new_head = build_head_index(orig_head)
    else:
        new_head = build_head_page(orig_head, critical_css, lcp_preload)
    
    new_body = optimize_body(orig_body)
    
    # Rebuild full HTML
    doctype = '<!DOCTYPE html>'
    lang = re.search(r'<html([^>]*)>', html)
    lang_attr = lang.group(1) if lang else ' lang="en-US"'
    
    result = f'{doctype}\n<html{lang_attr}>\n{new_head}\n<body>{new_body}</body>\n</html>'
    
    # Remove excessive blank lines (keep structure readable)
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(result)
    
    size = os.path.getsize(path)
    print(f"DONE: {os.path.basename(path)} -> {size:,} bytes")

# ── Also update style.min.css to add font-display:swap if missing ─────────────
def fix_font_display(css_path):
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()
    if '@font-face' in css and 'font-display' not in css:
        css = css.replace('@font-face{', '@font-face{font-display:swap;')
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css)
        print(f"DONE: Added font-display:swap to {os.path.basename(css_path)}")

# ── Run optimizations ──────────────────────────────────────────────────────────
print("=== Starting global PageSpeed optimizations ===\n")

optimize_file(
    os.path.join(BASE, 'index.html'),
    is_index=True
)

optimize_file(
    os.path.join(BASE, 'blog.html'),
    critical_css=CRITICAL_BLOG,
    lcp_preload='https://i.ibb.co/7dFpH3yc/Chat-GPT-Image-May-14-2026-02-46-52-AM.png'
)

optimize_file(
    os.path.join(BASE, 'pricing.html'),
    critical_css=CRITICAL_PAGE
)

optimize_file(
    os.path.join(BASE, 'faq.html'),
    critical_css=CRITICAL_PAGE
)

fix_font_display(os.path.join(BASE, 'style.min.css'))

print("\n=== All optimizations complete! ===")
