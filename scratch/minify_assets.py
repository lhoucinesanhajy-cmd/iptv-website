import re
import os

def minify_css(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{:;,])\s*', r'\1', css)
    return css.strip()

def minify_js(js):
    # Very simple JS minification (removes comments and extra spaces)
    js = re.sub(r'//.*', '', js)
    js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
    js = re.sub(r'\s+', ' ', js)
    return js.strip()

def process_file(path, minifier):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    minified = minifier(content)
    with open(path.replace('.css', '.min.css').replace('.js', '.min.js'), 'w', encoding='utf-8') as f:
        f.write(minified)
    return minified

css_path = 'c:/Users/admin/Desktop/iptv-website/style.css'
js_path = 'c:/Users/admin/Desktop/iptv-website/script.js'

minified_css = process_file(css_path, minify_css)
process_file(js_path, minify_js)

# Extract critical CSS (approx first 600 lines of original)
# We'll just take the first 10000 characters of the minified CSS as a heuristic for critical CSS
# Or better, we can take the parts we identified.
# For simplicity, I'll just take the beginning of the minified CSS that covers reset, header, and hero.
critical_end = minified_css.find('.hero-img-placeholder{') + 500 # rough estimate
critical_css = minified_css[:critical_end]
# Ensure it ends with a closing brace if possible
if '}' in critical_css:
    critical_css = critical_css[:critical_css.rfind('}')+1]

with open('c:/Users/admin/Desktop/iptv-website/critical-home.css', 'w', encoding='utf-8') as f:
    f.write(critical_css)

print("Minification and critical CSS extraction complete.")
