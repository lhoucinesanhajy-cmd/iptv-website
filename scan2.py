import os, sys

WORKSPACE = r"c:\Users\admin\Desktop\iptv-website"
EXTENSIONS = {".html", ".css", ".js"}

sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", buffering=1)

results = {}
for root, dirs, files in os.walk(WORKSPACE):
    dirs[:] = [d for d in dirs if not d.startswith(".")]
    for fname in files:
        if os.path.splitext(fname)[1].lower() not in EXTENSIONS:
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        bad_positions = [i for i, c in enumerate(content) if c == "\uFFFD"]
        if bad_positions:
            results[fname] = []
            for pos in bad_positions[:5]:
                ctx = content[max(0,pos-30):pos+30].replace("\n"," ").replace("\r","")
                results[fname].append("  pos " + str(pos) + ": [..." + ctx + "...]")

if results:
    print("Files with U+FFFD replacement chars:")
    for fname, samples in results.items():
        print("  FILE: " + fname)
        for s in samples:
            print(s)
else:
    print("ALL CLEAN - no replacement chars found!")
