import os
import glob

GA_CODE = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-F4Z3HZTWLR"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-F4Z3HZTWLR');
</script>
"""

def add_ga_to_files(directory):
    html_files = glob.glob(os.path.join(directory, '**', '*.html'), recursive=True)
    count = 0
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'G-F4Z3HZTWLR' in content:
                continue
                
            if '</head>' in content:
                new_content = content.replace('</head>', f'{GA_CODE}</head>')
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1
                print(f"Updated {file_path}")
            else:
                print(f"Warning: </head> not found in {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print(f"Successfully updated {count} files.")

if __name__ == "__main__":
    add_ga_to_files(r'c:\Users\admin\Desktop\iptv-website')
