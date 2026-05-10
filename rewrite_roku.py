import re

with open(r'c:\Users\admin\Desktop\iptv-website\blog\fix-iptv-error-401.html', 'r', encoding='utf-8') as f:
    template = f.read()

header_part = template.split('<main class="article-container">')[0]
footer_part = template.split('</main>')[1]

with open(r'c:\Users\admin\Desktop\iptv-website\blog\roku-iptv-setup.html', 'r', encoding='utf-8') as f:
    roku = f.read()

# Extract content from roku
body_content = re.search(r'<body>(.*?)</body>', roku, re.DOTALL).group(1)

# we need to remove the <article> tag and just keep its inner content
article_content_match = re.search(r'<article>(.*?)</article>', body_content, re.DOTALL)
if article_content_match:
    inner_content = article_content_match.group(1)
else:
    inner_content = body_content

# remove the h1 and article-meta and img since we will reconstruct them
h1_match = re.search(r'<h1>(.*?)</h1>', inner_content)
h1_text = h1_match.group(1) if h1_match else "How to Setup IPTV on Roku TV: The Only Working Methods in 2026"

# remove them from inner_content
inner_content = re.sub(r'<h1>.*?</h1>', '', inner_content, count=1, flags=re.DOTALL)
inner_content = re.sub(r'<div class="article-meta">.*?</div>', '', inner_content, count=1, flags=re.DOTALL)
inner_content = re.sub(r'<img src="https://i.ibb.co/PshxxysR/Chat-GPT-Image-May-10-2026-05-01-00-PM.png".*?>', '', inner_content, count=1, flags=re.DOTALL)

# Now build the new main block
main_block = f"""
    <main class="article-container">
        <a href="../blog.html" style="display: inline-block; margin-bottom: 20px; color: #a855f7; text-decoration: none; font-weight: 600;"><i class="fa-solid fa-arrow-left"></i> Back to Blog</a>
        <div class="article-header">
            <span class="article-tag">IPTV Tutorials</span>
            <h1 class="article-title">{h1_text}</h1>
            <div class="article-meta">
                <span><i class="fa-regular fa-calendar"></i> May 10, 2026</span>
                <span><i class="fa-regular fa-clock"></i> 15 min read</span>
            </div>
        </div>

        <div class="article-content">
            <img src="https://i.ibb.co/PshxxysR/Chat-GPT-Image-May-10-2026-05-01-00-PM.png" alt="{h1_text}" style="width:100%; border-radius: 12px; margin-bottom: 3rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
            {inner_content}
        </div>
    </main>
"""

# Let's fix the title and description in the header part
header_part = re.sub(r'<title>.*?</title>', f'<title>{h1_text} | OttOcean IPTV</title>', header_part, flags=re.DOTALL)
header_part = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="Learn the definitive, step-by-step methods to setup IPTV on your Roku TV in 2026. Discover workarounds, hidden apps, and the ultimate hardware fixes.">', header_part)

new_html = header_part + main_block + footer_part

with open(r'c:\Users\admin\Desktop\iptv-website\blog\roku-iptv-setup.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Done rewriting roku article.")
