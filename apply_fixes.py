import os, glob, re

script_dir = r"c:\Users\admin\Desktop\iptv-website"
html_files = glob.glob(os.path.join(script_dir, '*.html'))

for fp in html_files:
    with open(fp, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 1. Character Encoding Fix
    text = text.replace('â€“', '–')
    text = text.replace('â€”', '–') # user asked for a clean dash
    text = text.replace('â‚¬', '€')
    
    # Ensure <meta charset="UTF-8"> is first tag in head
    text = re.sub(r'<meta\s+charset="UTF-8"\s*/?>\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'(<head>)\s*', r'\1\n    <meta charset="UTF-8">\n    ', text, flags=re.IGNORECASE)
    
    # 2. Content Accuracy Check - OUR PLANS
    text = text.replace('OttOcean 3 Months', '3 Months – €39')
    text = text.replace('OttOcean 6 Months', '6 Months – €49')
    text = text.replace('OttOcean 12 Months', '12 Months – €65')
    
    # 3. Footer description
    text = re.sub(
        r'<p class="footer-tagline">.*?</p>', 
        '<p class="footer-tagline">Premium IPTV streaming – 15,000+ channels, 4K quality, 99.9% uptime.</p>', 
        text, 
        flags=re.DOTALL
    )
    
    # 4. Footer Titles
    text = text.replace('<h4 class="footer-col-title">OttOcean Links</h4>', '<h4 class="footer-col-title">QUICK LINKS</h4>')
    text = text.replace('<h4 class="footer-col-title">Our Plans</h4>', '<h4 class="footer-col-title">OUR PLANS</h4>')
    text = text.replace('<h4 class="footer-col-title">Contact</h4>', '<h4 class="footer-col-title">GET IN TOUCH</h4>')

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)

print(f"Processed {len(html_files)} files.")
