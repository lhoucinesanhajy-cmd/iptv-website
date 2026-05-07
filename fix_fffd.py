import os, sys, re

WORKSPACE = r"c:\Users\admin\Desktop\iptv-website"
EXTENSIONS = {".html", ".css", ".js"}

sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", buffering=1)

# Manual replacement map for all U+FFFD occurrences in context
# Based on the scan: em dashes, euro signs, and broken emojis
# Pattern: (search_string_with_fffd, replacement)
# We identify them from context

CONTEXT_FIXES = [
    # Em dash in descriptive contexts (the most common FFFD)
    # "4K Quality \uFFFD the ultimate" -> "4K Quality \u2013 the ultimate"
    # We'll replace FFFD between word chars with en dash
    # Euro sign before numbers
    ("\uFFFD39", "\u20AC39"),
    ("\uFFFD49", "\u20AC49"),
    ("\uFFFD65", "\u20AC65"),
    # En dashes in titles (Contact Us \uFFFD OttOcean)
    ("Contact Us \uFFFD OttOcean", "Contact Us \u2013 OttOcean"),
    ("FAQ \uFFFD OttOcean", "FAQ \u2013 OttOcean"),
    ("Pricing Plans \uFFFD OttOcean", "Pricing Plans \u2013 OttOcean"),
    ("IPTV Tips \uFFFD Guides", "IPTV Tips \u2013 Guides"),
    # Footer tagline
    ("IPTV streaming \uFFFD 15,000+", "IPTV streaming \u2013 15,000+"),
    # Hero / content descriptions
    ("4K Quality \uFFFD the ultimate", "4K Quality \u2013 the ultimate"),
    ("4K Ultra HD \uFFFD Stable Stream", "4K Ultra HD \u00B7 Stable Stream"),
    ("live sports \uFFFD all in stunning", "live sports \u2013 all in stunning"),
    # Blog post em dashes (narrative text)
    ("main network\uFFFDwhere", "main network \u2014 where"),
    ("content\uFFFDremains", "content \u2014 remains"),
    ("approaches\uFFFDor", "approaches \u2014 or"),
    ("taken\uFFFDthe", "taken \u2014 the"),
    ("Wi-Fi\uFFFDfrom", "Wi-Fi \u2014 from"),
    ("Smart TV\uFFFDis", "Smart TV \u2014 is"),
    ("platform\uFFFDonce", "platform \u2014 once"),
    ("throttling\uFFFDread", "throttling \u2014 read"),
    # Script.js and CSS comments
    ("Navbar \uFFFD scroll", "Navbar \u2013 scroll"),
    ("MARQUEE GENERATOR \uFFFD RELIABLE", "MARQUEE GENERATOR \u2013 RELIABLE"),
    ("Wrapper li \uFFFD pushes", "Wrapper li \u2013 pushes"),
    ("SECTION 1 \uFFFD CONTENT", "SECTION 1 \u2013 CONTENT"),
    ("transition \uFFFD cubic", "transition \u2013 cubic"),
    ("colours \uFFFD easy", "colours \u2013 easy"),
    ("variants \uFFFD background", "variants \u2013 background"),
    # Contact page
    ("Reach out \uFFFD we", "Reach out \u2013 we"),
    ("no bots \uFFFD real", "no bots \u2013 real"),
    ("Months \uFFFD \uFFFD39", "Months \u2013 \u20AC39"),
    ("Months \uFFFD \uFFFD49", "Months \u2013 \u20AC49"),
    ("Months \uFFFD \uFFFD65", "Months \u2013 \u20AC65"),
    # Blog/FAQ page-hero-tag emojis that are broken (half of a surrogate)
]

# Additionally fix remaining FFFD in pricing/plans context
REGEX_FIXES = [
    # "X Months \uFFFD \uFFFDNN" -> "X Months – €NN"
    (r"(\d+) Months \uFFFD \uFFFD(\d+)", r"\1 Months \u2013 \u20AC\2"),
    # Isolated FFFD between word chars -> em dash
    (r"(\w)\uFFFD(\w)", r"\1\u2014\2"),
    # FFFD surrounded by spaces -> en dash
    (r" \uFFFD ", " \u2013 "),
    # FFFD at end of sentence snippets near letters
    (r"(\w)\uFFFD ", r"\1\u2013 "),
    (r" \uFFFD(\w)", r" \u2013\1"),
]

# Emoji broken fragments (the half-emoji patterns from faq/blog)
EMOJI_REGEX_FIXES = [
    # "\uFFFD? Tips" -> "📰 Tips" (newspaper emoji for blog)
    (r"\uFFFD\? Tips & Guides", "\U0001F4F0 Tips & Guides"),
    (r"\uFFFD\?Tips", "\U0001F4F0 Tips"),
    # "\uFFFD?\uFFFD Got Questions" -> "🤔 Got Questions"
    (r"\uFFFD\?\uFFFD Got Questions\?", "\U0001F914 Got Questions?"),
    (r"\uFFFD?\uFFFD Got Questions", "\U0001F914 Got Questions"),
    # "\uFFFD? Global Coverage" -> "🌍 Global Coverage"
    (r"\uFFFD\? Global Coverage", "\U0001F30D Global Coverage"),
    # "15,000+ channels for 24 hours \uFFFD no payment" -> em dash
    (r"24 hours \uFFFD no", "24 hours \u2014 no"),
    # FontAwesome comment
    (r"FontAwesome 6 Free \uFFFD used", "FontAwesome 6 Free \u2013 used"),
    # Blog og:title en dash
    (r"Tips &amp; Guides Blog \uFFFD OttOcean", "Tips &amp; Guides Blog \u2013 OttOcean"),
    (r"Tips & Guides Blog \uFFFD OttOcean", "Tips & Guides Blog \u2013 OttOcean"),
    # flexible, no contracts
    (r"months\) \uFFFD flexible", "months) \u2013 flexible"),
    # Pricing meta description
    (r"plans from \uFFFD(\d+)", r"plans from \u20AC\1"),
    (r"months\), \uFFFD(\d+)", r"months), \u20AC\1"),
    (r"months\) or \uFFFD(\d+)", r"months) or \u20AC\1"),
]

def apply_fixes(content):
    # Apply literal fixes first
    for bad, good in CONTEXT_FIXES:
        content = content.replace(bad, good)
    # Apply regex fixes
    for pattern, repl in REGEX_FIXES + EMOJI_REGEX_FIXES:
        content = re.sub(pattern, repl, content)
    return content

processed = 0
for root, dirs, files in os.walk(WORKSPACE):
    dirs[:] = [d for d in dirs if not d.startswith(".")]
    for fname in files:
        if os.path.splitext(fname)[1].lower() not in EXTENSIONS:
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        
        before_count = content.count("\uFFFD")
        if before_count == 0:
            print("SKIP (clean): " + fname)
            continue
        
        fixed = apply_fixes(content)
        after_count = fixed.count("\uFFFD")
        
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(fixed)
        
        print("Fixed: " + fname + " (" + str(before_count) + " -> " + str(after_count) + " FFFD chars)")
        processed += 1

print("\nDone. " + str(processed) + " files patched.")
