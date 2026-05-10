import re

def process():
    with open('blog.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the blog-grid
    match = re.search(r'(<div class="blog-grid">)(.*?)(    </div>\s*<!-- CTA to try the service -->)', html, re.DOTALL)
    if not match:
        print("Could not find blog-grid")
        return
        
    grid_start = match.group(1)
    grid_content = match.group(2)
    grid_end = match.group(3)
    
    parts = grid_content.split('</article>')
    articles = []
    for part in parts:
        if '<article' in part:
            article_str = part[part.find('<article'):] + '</article>'
            articles.append(article_str)
            
    print(f"Parsed {len(articles)} articles.")
    
    page1_articles = articles[:6]
    page2_articles = articles[6:]
    
    pagination_html_1 = """
    <div class="pagination">
        <a href="blog.html" class="active">1</a>
        <a href="blog-page-2.html">2</a>
        <a href="blog-page-2.html" class="next">Next &rarr;</a>
    </div>
"""
    
    pagination_html_2 = """
    <div class="pagination">
        <a href="blog.html" class="prev">&larr; Prev</a>
        <a href="blog.html">1</a>
        <a href="blog-page-2.html" class="active">2</a>
    </div>
"""

    pagination_css = """
        /* ---- Pagination styles ---- */
        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin: 40px auto 80px;
        }
        .pagination a {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #fff;
            padding: 10px 18px;
            border-radius: 8px;
            text-decoration: none;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .pagination a:hover, .pagination a.active {
            background: rgba(168, 85, 247, 0.2);
            border-color: #a855f7;
            box-shadow: 0 0 15px rgba(168, 85, 247, 0.3);
        }
    </style>"""

    before_grid = html[:match.start(0) + len(grid_start)]
    after_grid = html[match.end(2):]
    
    # Check if CSS was already injected (since script was run once, </style> might have been replaced)
    if '/* ---- Pagination styles ---- */' not in before_grid:
        before_grid = before_grid.replace('</style>', pagination_css)

    page1_html = before_grid + '\n' + '\n'.join(page1_articles) + '\n' + after_grid
    
    # Check if <link rel="next" is already there
    if '<link rel="next"' not in page1_html:
        page1_html = page1_html.replace('</head>', '    <link rel="next" href="blog-page-2.html">\n</head>')

    # Regex replace for pagination 1
    page1_html = re.sub(r'(</div>\s*)(<!-- CTA to try the service -->)', r'\1' + pagination_html_1 + r'\n\2', page1_html)

    page2_html = before_grid + '\n' + '\n'.join(page2_articles) + '\n' + after_grid
    
    if '<link rel="prev"' not in page2_html:
        page2_html = page2_html.replace('</head>', '    <link rel="prev" href="blog.html">\n</head>')
        
    page2_html = re.sub(r'<title>.*?</title>', '<title>Blog - Page 2 - OttOcean IPTV</title>', page2_html)
    page2_html = re.sub(r'(</div>\s*)(<!-- CTA to try the service -->)', r'\1' + pagination_html_2 + r'\n\2', page2_html)

    with open('blog.html', 'w', encoding='utf-8') as f:
        f.write(page1_html)
        
    with open('blog-page-2.html', 'w', encoding='utf-8') as f:
        f.write(page2_html)

    print("Successfully created blog.html and blog-page-2.html")

if __name__ == '__main__':
    process()
