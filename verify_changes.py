import os

BASE = r"c:\Users\admin\Desktop\iptv-website"
files = [
    "index.html", "blog.html", "contact.html", "faq.html", "pricing.html",
    "blog-post-1.html", "blog-post-2.html", "blog-post-3.html",
    "blog-post-4.html", "firestick-guide.html"
]

for fn in files:
    fp = os.path.join(BASE, fn)
    with open(fp, encoding="utf-8") as f:
        c = f.read()
    has_gsc    = "google-site-verification" in c
    has_can    = 'rel="canonical"' in c
    has_old_fa = "font-awesome/6.0.0" in c
    print(f"{fn}: GSC={has_gsc}, canonical={has_can}, old_FA={has_old_fa}")
