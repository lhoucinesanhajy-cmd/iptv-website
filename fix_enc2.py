import os, re, sys

WORKSPACE = r"c:\Users\admin\Desktop\iptv-website"

# Mojibake -> correct mapping (using unicode escapes to avoid encoding issues in script itself)
REPLACEMENTS = [
    ("\xf0\x9f\x94\xa5", "\U0001F525"),  # fire emoji
    ("\xf0\x9f\x93\xba", "\U0001F4FA"),  # TV emoji
    ("\xf0\x9f\x8c\x8d", "\U0001F30D"),  # globe
    ("\xf0\x9f\x8e\xac", "\U0001F3AC"),  # clapper
    ("\xf0\x9f\x92\xac", "\U0001F4AC"),  # speech bubble
    ("\xf0\x9f\x8f\x86", "\U0001F3C6"),  # trophy
    ("\xe2\x86\x92", "\u2192"),           # right arrow
    ("\xe2\x86\x94", "\u2194"),           # left-right arrow
    ("\xe2\x86\x93", "\u2193"),           # down arrow
    ("\xe2\x86\x90", "\u2190"),           # left arrow
    ("\xe2\x86\x91", "\u2191"),           # up arrow
    ("\xe2\x80\x94", "\u2014"),           # em dash
    ("\xe2\x80\x93", "\u2013"),           # en dash
    ("\xe2\x80\x98", "\u2018"),           # left single quote
    ("\xe2\x80\x99", "\u2019"),           # right single quote
    ("\xe2\x80\x9c", "\u201C"),           # left double quote
    ("\xe2\x80\x9d", "\u201D"),           # right double quote
    ("\xe2\x80\xa6", "\u2026"),           # ellipsis
    ("\xe2\x80\xa2", "\u2022"),           # bullet
    ("\xe2\x84\xa2", "\u2122"),           # TM
    ("\xc2\xa9", "\u00A9"),               # copyright
    ("\xc2\xae", "\u00AE"),               # registered
    ("\xc2\xb0", "\u00B0"),               # degree
    ("\xe2\x82\xac", "\u20AC"),           # euro
    ("\xc2\xa3", "\u00A3"),               # pound
    ("\xe2\x98\x85", "\u2605"),           # filled star
    ("\xe2\x98\x86", "\u2606"),           # empty star
    ("\xe2\x9c\x94", "\u2714"),           # heavy check
    ("\xe2\x9c\x97", "\u2717"),           # ballot x
    ("\xe2\x9c\x85", "\u2705"),           # white check mark
    ("\xe2\x9d\x8c", "\u274C"),           # cross mark
    ("\xc2\xb7", "\u00B7"),               # middle dot
    ("\xc2\xbb", "\u00BB"),               # right guillemet
    ("\xc2\xab", "\u00AB"),               # left guillemet
    ("\xc3\xa9", "\u00E9"),               # e acute
    ("\xc3\xa8", "\u00E8"),               # e grave
    ("\xc3\xa0", "\u00E0"),               # a grave
    ("\xc3\xa7", "\u00E7"),               # c cedilla
    ("\xc3\xbc", "\u00FC"),               # u umlaut
    ("\xc3\xb6", "\u00F6"),               # o umlaut
    ("\xc3\xa4", "\u00E4"),               # a umlaut
    ("\xc3\xb1", "\u00F1"),               # n tilde
    ("\xf0\x9f\x93\xb1", "\U0001F4F1"),  # mobile phone
    ("\xf0\x9f\x92\xbb", "\U0001F4BB"),  # laptop
    ("\xf0\x9f\x8c\x9f", "\U0001F31F"),  # glowing star
]

EXTENSIONS = {".html", ".css", ".js"}

def fix_content(raw_bytes):
    # Step 1: decode as latin-1 (lossless)
    text = raw_bytes.decode("latin-1")
    
    # Step 2: try double-decode (the main fix for mojibake)
    # Each char in latin-1 maps 1:1 to its byte value,
    # so re-encoding to latin-1 gives back the original bytes,
    # then decode as utf-8 fixes the mojibake.
    try:
        fixed = text.encode("latin-1").decode("utf-8")
        text = fixed
    except (UnicodeEncodeError, UnicodeDecodeError):
        # If double-decode fails, apply manual table on the raw bytes
        for bad_bytes, good_char in REPLACEMENTS:
            text = text.replace(bad_bytes, good_char)
    
    return text

def ensure_charset_meta(content, filepath):
    if not filepath.endswith(".html"):
        return content
    # Remove existing charset meta tags
    content = re.sub(r'<meta\s+charset=["\']?[^"\'>\s]+["\']?\s*/?>', '', content, flags=re.IGNORECASE)
    # Insert after <head>
    content = re.sub(r'(<head[^>]*>)', r'\1\n    <meta charset="UTF-8">', content, count=1, flags=re.IGNORECASE)
    return content

processed = 0
for root, dirs, files in os.walk(WORKSPACE):
    dirs[:] = [d for d in dirs if not d.startswith(".")]
    for fname in files:
        if os.path.splitext(fname)[1].lower() not in EXTENSIONS:
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, "rb") as f:
            raw = f.read()
        # Strip BOM
        if raw.startswith(b"\xef\xbb\xbf"):
            raw = raw[3:]
        fixed = fix_content(raw)
        fixed = ensure_charset_meta(fixed, fpath)
        out = fixed.encode("utf-8")
        with open(fpath, "wb") as f:
            f.write(out)
        print("Fixed:", fname)
        processed += 1

print(f"\nDone. Processed {processed} files.")
