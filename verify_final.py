import sys, re

files_to_check = [
    r"c:\Users\admin\Desktop\iptv-website\index.html",
    r"c:\Users\admin\Desktop\iptv-website\contact.html",
    r"c:\Users\admin\Desktop\iptv-website\pricing.html",
    r"c:\Users\admin\Desktop\iptv-website\faq.html",
    r"c:\Users\admin\Desktop\iptv-website\blog.html",
    r"c:\Users\admin\Desktop\iptv-website\firestick-guide.html",
    r"c:\Users\admin\Desktop\iptv-website\blog-post-1.html",
    r"c:\Users\admin\Desktop\iptv-website\blog-post-2.html",
]

EXPECTED_EMOJIS = {
    "\U0001F525": "fire",
    "\U0001F4FA": "TV",
    "\U0001F30D": "globe",
    "\U0001F3AC": "clapper",
    "\U0001F4AC": "speech bubble",
    "\u2192": "right arrow",
    "\u2014": "em dash",
    "\u2013": "en dash",
    "\u2019": "apostrophe",
    "\u20AC": "euro",
    "\u2605": "star",
    "\u2714": "check",
    "\u00A9": "copyright",
}

for fpath in files_to_check:
    fname = fpath.split("\\")[-1]
    with open(fpath, "rb") as f:
        raw = f.read()
    # Validate UTF-8
    try:
        content = raw.decode("utf-8")
        valid = "UTF-8 OK"
    except:
        content = raw.decode("latin-1")
        valid = "NOT UTF-8!"
    
    # Check charset meta
    has_charset = bool(re.search(r'<meta\s+charset=["\']?UTF-8', content, re.IGNORECASE))
    
    # Check for remaining mojibake (double-encoded sequences)
    # A mojibake pattern: a non-ASCII char that when encoded to cp1252 and decoded as utf-8 gives a different char
    non_ascii = [(i, c, hex(ord(c))) for i, c in enumerate(content) if ord(c) > 127]
    
    # Group by category
    emojis_found = [c for _, c, _ in non_ascii if ord(c) > 0x2000]
    special_found = [c for _, c, _ in non_ascii if 0x80 < ord(c) <= 0x2000]
    
    sys.stdout.write(fname + ":\n")
    sys.stdout.write("  " + valid + " | charset meta: " + str(has_charset) + "\n")
    sys.stdout.write("  Emoji/symbol chars: " + str(len(emojis_found)) + "\n")
    sys.stdout.write("  Special chars (€, —, etc): " + str(len(special_found)) + "\n")
    if emojis_found:
        sample = "  Sample: " + " ".join(emojis_found[:8]) + "\n"
        sys.stdout.buffer.write(sample.encode("utf-8"))
    sys.stdout.write("\n")
