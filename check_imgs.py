import os
import re

html_files = []
for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or '.git' in root: continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

for fpath in html_files:
    if 'blog' in fpath or fpath.endswith('guide.html'):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        imgs = re.findall(r'<img[^>]+>', content)
        if imgs:
            print(f"{os.path.basename(fpath)}: {imgs[0]}")
