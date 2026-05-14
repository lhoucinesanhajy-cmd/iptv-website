import os
import re

directory = "c:\\Users\\admin\\Desktop\\iptv-website"

geo_meta = """<meta name="geo.region" content="US" />
    <meta name="geo.placename" content="United States" />"""

schema_markup = """
    <!-- Schema Markup for US -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "Organization",
          "name": "Ottocean",
          "url": "https://ottocean.sbs/",
          "logo": "https://ottocean.sbs/logo.png",
          "areaServed": {
            "@type": "Country",
            "name": "United States"
          }
        },
        {
          "@type": "Service",
          "name": "IPTV Service USA",
          "provider": {
            "@type": "Organization",
            "name": "Ottocean"
          },
          "areaServed": {
            "@type": "Country",
            "name": "United States"
          },
          "description": "Premium IPTV service with US Sports Networks and local channels."
        }
      ]
    }
    </script>
"""

# Gather all HTML files, including those in blog/ folder
html_files = []
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".html"):
            html_files.append(os.path.join(root, file))

for file_path in html_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1 & 5: Language tag
    content = re.sub(r'<html[^>]*>', '<html lang="en-US">', content)
    
    # 2: Geo Meta
    if "geo.region" not in content:
        content = content.replace("</head>", f"    {geo_meta}\n{schema_markup}</head>")
        
    # Content Localization for the large articles
    if "setup-iptv-apple-tv-4k" in file_path or "watch-ufc-premier-league" in file_path:
        # Just append some keywords safely, or replace some generic terms
        if "Best IPTV USA" not in content:
            content = content.replace("IPTV service", "IPTV service (voted Best IPTV USA)")
            content = content.replace("streaming regulations", "FCC streaming regulations")
            content = content.replace("Sports Networks", "US Sports Networks")
            # If not matched, just append to a paragraph
            if "US Sports Networks" not in content:
                content = content.replace("<p>", "<p>Including access to major US Sports Networks and compliant with FCC streaming regulations, ensuring the Best IPTV USA experience. ", 1)
        
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Updated HTML files for USA SEO.")
