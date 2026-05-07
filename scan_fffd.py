import os, sys

WORKSPACE = r"c:\Users\admin\Desktop\iptv-website"
EXTENSIONS = {".html", ".css", ".js"}

results = {}
for root, dirs, files in os.walk(WORKSPACE):
    dirs[:] = [d for d in dirs if not d.startswith(".")]
    for fname in files:
        if os.path.splitext(fname)[1].lower() not in EXTENSIONS:
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        # Find replacement chars (U+FFFD = decode errors)
        bad_positions = [i for i, c in enumerate(content) if c == "\uFFFD"]
        if bad_positions:
            results[fname] = []
            for pos in bad_positions[:5]:
                ctx = content[max(0,pos-20):pos+20].replace("\n","\\n").replace("\r","\\r")
                results[fname].append("  pos " + str(pos) + ": " + repr(ctx))

if results:
    sys.stdout.write("Files with replacement chars (UFFFD):\n")
    for fname, samples in results.items():
        sys.stdout.write("  " + fname + ":\n")
        for s in samples:
            sys.stdout.write(s + "\n")
else:
    sys.stdout.write("No replacement chars found - all clean!\n")
