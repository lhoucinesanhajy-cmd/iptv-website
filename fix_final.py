import os, re, sys

WORKSPACE = r"c:\Users\admin\Desktop\iptv-website"
EXTENSIONS = {".html", ".css", ".js"}

def fix_mojibake(raw_bytes):
    """
    Correct decode chain:
      raw bytes (bad UTF-8) -> decode as UTF-8 -> encode as cp1252 -> decode as UTF-8
    This reverses: original UTF-8 bytes -> misread as cp1252 chars -> re-saved as UTF-8
    """
    # Strip UTF-8 BOM
    if raw_bytes.startswith(b'\xef\xbb\xbf'):
        raw_bytes = raw_bytes[3:]

    # First, verify file is valid UTF-8 (it should be after previous script run)
    try:
        step1 = raw_bytes.decode('utf-8')
    except UnicodeDecodeError:
        # Fall back: read as latin-1
        step1 = raw_bytes.decode('latin-1')

    # Now re-encode as cp1252 to get back the original raw bytes
    try:
        step2 = step1.encode('cp1252', errors='replace')
    except Exception:
        step2 = step1.encode('latin-1', errors='replace')

    # Now decode those bytes as UTF-8 to get the real characters
    try:
        step3 = step2.decode('utf-8', errors='replace')
        return step3
    except Exception:
        return step1  # give up, return as-is

def ensure_charset_meta(content, filepath):
    if not filepath.endswith('.html'):
        return content
    # Remove existing charset meta tags (all of them, wherever they are)
    content = re.sub(
        r'\s*<meta\s+charset=["\']?[^"\'>\s]+["\']?\s*/?>',
        '',
        content,
        flags=re.IGNORECASE
    )
    # Insert right after <head>
    content = re.sub(
        r'(<head[^>]*>)',
        r'\1\n    <meta charset="UTF-8">',
        content,
        count=1,
        flags=re.IGNORECASE
    )
    return content

processed = 0
errors = 0
for root, dirs, files in os.walk(WORKSPACE):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for fname in files:
        ext = os.path.splitext(fname)[1].lower()
        if ext not in EXTENSIONS:
            continue
        fpath = os.path.join(root, fname)
        try:
            with open(fpath, 'rb') as f:
                raw = f.read()
            fixed = fix_mojibake(raw)
            fixed = ensure_charset_meta(fixed, fpath)
            out_bytes = fixed.encode('utf-8')
            with open(fpath, 'wb') as f:
                f.write(out_bytes)
            # Count non-ASCII chars to verify emojis are in
            non_ascii = sum(1 for c in fixed if ord(c) > 127)
            sys.stdout.write("Fixed: " + fname + " (non-ascii chars: " + str(non_ascii) + ")\n")
            processed += 1
        except Exception as e:
            sys.stdout.write("ERROR: " + fname + " - " + str(e) + "\n")
            errors += 1

sys.stdout.write("\nDone. Processed: " + str(processed) + ", Errors: " + str(errors) + "\n")
