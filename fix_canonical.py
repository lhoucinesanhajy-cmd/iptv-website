import glob, re, os

# 1. Update script.js with redirect
script_js = 'script.js'
with open(script_js, 'r', encoding='utf-8') as f:
    content = f.read()

redirect_code = '''/* Force HTTPS and WWW */
if (window.location.hostname.includes('ottocean.sbs')) {
    if (window.location.hostname !== 'www.ottocean.sbs' || window.location.protocol !== 'https:') {
        window.location.replace('https://www.ottocean.sbs' + window.location.pathname + window.location.search);
    }
}
'''
if 'Force HTTPS and WWW' not in content:
    with open(script_js, 'w', encoding='utf-8') as f:
        f.write(redirect_code + '\n' + content)

# 2. Fix canonical tags in all HTML files
html_files = glob.glob('*.html') + glob.glob('blog/*.html')
for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        html = file.read()
    
    # Expected canonical URL
    if f == 'index.html':
        expected_url = 'https://www.ottocean.sbs/'
    else:
        # replace \ with / for windows paths
        url_path = f.replace(os.sep, '/')
        expected_url = f'https://www.ottocean.sbs/{url_path}'
        
    canonical_tag = f'<link rel="canonical" href="{expected_url}">'
    
    # check if canonical exists
    if '<link rel="canonical"' in html:
        # replace it
        html = re.sub(r'<link rel="canonical".*?>', canonical_tag, html)
    else:
        # add before </head>
        html = html.replace('</head>', f'    {canonical_tag}\n</head>')
        
    with open(f, 'w', encoding='utf-8') as file:
        file.write(html)
