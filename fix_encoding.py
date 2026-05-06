# fix_encoding.py
# Fixes UTF-8 mojibake in all HTML files in the same directory.
# The broken sequences are UTF-8 multi-byte characters mis-interpreted as Latin-1/Windows-1252.
import os, glob

# Each tuple: (broken_string_as_it_appears_in_file, correct_replacement)
REPLACEMENTS = [
    # --- Currency / punctuation ---
    ("\u00e2\u0080\u0093", "\u2013"),   # â€" -> en dash –
    ("\u00e2\u0080\u0094", "\u2014"),   # â€" -> em dash —
    ("\u00e2\u0080\u0099", "\u2019"),   # â€™ -> right single quote '
    ("\u00e2\u0080\u0098", "\u2018"),   # â€˜ -> left single quote '
    ("\u00e2\u0080\u009c", "\u201c"),   # â€œ -> left double quote "
    ("\u00e2\u0080\u009d", "\u201d"),   # â€ -> right double quote "
    ("\u00e2\u0080\u00a2", "\u2022"),   # â€¢ -> bullet •
    ("\u00e2\u0080\u00a6", "\u2026"),   # â€¦ -> ellipsis …
    ("\u00c2\u00b7",        "\u00b7"),  # Â· -> middle dot ·
    ("\u00c2\u00b0",        "\u00b0"),  # Â° -> degree °
    ("\u00c2\u00a9",        "\u00a9"),  # Â© -> copyright ©
    ("\u00c2\u00ae",        "\u00ae"),  # Â® -> registered ®
    ("\u00c2\u00a3",        "\u00a3"),  # Â£ -> pound £
    ("\u00e2\u0082\u00ac",  "\u20ac"),  # â‚¬ -> euro €
    ("\u00c2\u00bd",        "\u00bd"),  # Â½ -> ½
    ("\u00c2\u00a0",        "\u00a0"),  # Â  -> non-breaking space
    ("\u00c2\u00bb",        "\u00bb"),  # Â» -> »
    ("\u00c2\u00ab",        "\u00ab"),  # Â« -> «

    # --- Arrows / UI symbols ---
    ("\u00e2\u0086\u0092", "\u2192"),   # â†' -> →
    ("\u00e2\u0080\u00ba", "\u203a"),   # â€º -> ›
    ("\u00e2\u0094\u0080", "\u2500"),   # â"€ -> ─
    ("\u00e2\u0098\u0085", "\u2605"),   # â˜… -> ★
    ("\u00e2\u0098\u0086", "\u2606"),   # â˜† -> ☆
    ("\u00e2\u009c\u00a6", "\u2726"),   # âœ¦ -> ✦
    ("\u00e2\u00ad\u0090", "\u2b50"),   # â­ -> ⭐
    ("\u00e2\u009d\u0093", "\u2753"),   # â" -> ❓
    ("\u00e2\u009d\u00a4", "\u2764"),   # â" -> ❤

    # --- 3-byte emoji mis-decoded (U+0080–U+07FF range) ---
    ("\u00e2\u009a\u00bd", "\u26bd"),   # âš½ -> ⚽ soccer ball
    ("\u00e2\u009c\u0093", "\u2713"),   # âœ" -> ✓ check mark
    ("\u00e2\u009c\u0094", "\u2714"),   # âœ" -> ✔ heavy check mark

    # --- 4-byte emoji mis-decoded as 4 Latin-1 chars ---
    # Basketball 🏀 U+1F3C0
    ("\u00f0\u009f\u008f\u0080", "\U0001f3c0"),
    # Soccer ⚽ (already above as 3-byte, but some encoders use 4-byte path)
    ("\u00f0\u009f\u008f\u00be", "\U0001f3fe"),
    # Racing car 🏎️ U+1F3CE
    ("\u00f0\u009f\u008f\u008e\u00ef\u00b8\u008f", "\U0001f3ce\ufe0f"),
    ("\u00f0\u009f\u008f\u008e", "\U0001f3ce"),
    # Boxing glove 🥊 U+1F94A
    ("\u00f0\u009f\u00a5\u008a", "\U0001f94a"),
    # Clapperboard 🎬 U+1F3AC
    ("\u00f0\u009f\u008e\u00ac", "\U0001f3ac"),
    # Performing arts 🎭 U+1F3AD
    ("\u00f0\u009f\u008e\u00ad", "\U0001f3ad"),
    # Rocket 🚀 U+1F680
    ("\u00f0\u009f\u009a\u0080", "\U0001f680"),
    # Fire 🔥 U+1F525
    ("\u00f0\u009f\u0094\u00a5", "\U0001f525"),
    # Laughing face 😂 U+1F602
    ("\u00f0\u009f\u0098\u0082", "\U0001f602"),
    # TV 📺 U+1F4FA
    ("\u00f0\u009f\u0093\u00ba", "\U0001f4fa"),
    # Globe 🌍 U+1F30D
    ("\u00f0\u009f\u008c\u008d", "\U0001f30d"),
    # Credit card 💳 U+1F4B3
    ("\u00f0\u009f\u0092\u00b3", "\U0001f4b3"),
    # Speech bubble 💬 U+1F4AC
    ("\u00f0\u009f\u0092\u00ac", "\U0001f4ac"),
    # Trophy 🏆 U+1F3C6
    ("\u00f0\u009f\u008f\u0086", "\U0001f3c6"),
    # Gold medal 🥇 U+1F947
    ("\u00f0\u009f\u00a5\u0087", "\U0001f947"),
    # Sparkles 💫 U+1F4AB
    ("\u00f0\u009f\u0092\u00ab", "\U0001f4ab"),
    # Glowing star 🌟 U+1F31F
    ("\u00f0\u009f\u008c\u009f", "\U0001f31f"),
    # Explosion 💥 U+1F4A5
    ("\u00f0\u009f\u0092\u00a5", "\U0001f4a5"),
    # Lock 🔒 U+1F512
    ("\u00f0\u009f\u0094\u0092", "\U0001f512"),
    # Target 🎯 U+1F3AF
    ("\u00f0\u009f\u008e\u00af", "\U0001f3af"),
    # Checkmark emoji ✅ U+2705
    ("\u00e2\u009c\u0085", "\u2705"),
    # Party popper 🎉 U+1F389
    ("\u00f0\u009f\u008e\u0089", "\U0001f389"),
    # Gem 💎 U+1F48E
    ("\u00f0\u009f\u0092\u008e", "\U0001f48e"),
    # Chart 📈 U+1F4C8
    ("\u00f0\u009f\u0093\u0088", "\U0001f4c8"),
    # Shield 🛡️ U+1F6E1
    ("\u00f0\u009f\u009b\u00a1\u00ef\u00b8\u008f", "\U0001f6e1\ufe0f"),
    # Satellite 📡 U+1F4E1
    ("\u00f0\u009f\u0093\u00a1", "\U0001f4e1"),
    # Antenna 📶 U+1F4F6
    ("\u00f0\u009f\u0093\u00b6", "\U0001f4f6"),
]

def fix_file(path):
    # Read raw bytes and decode as Latin-1 (to get the raw codepoints as-is)
    with open(path, 'rb') as f:
        raw = f.read()
    
    # The file is stored as UTF-8 but the CHARACTERS in it are the wrong ones.
    # We need to decode as UTF-8 first to get the Python string with the mangled chars.
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        print(f"  SKIP (not UTF-8): {path}")
        return False

    original = text
    for bad, good in REPLACEMENTS:
        text = text.replace(bad, good)

    if text != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    return False

script_dir = os.path.dirname(os.path.abspath(__file__))
html_files = glob.glob(os.path.join(script_dir, '*.html'))

total_fixed = 0
for fp in sorted(html_files):
    changed = fix_file(fp)
    name = os.path.basename(fp)
    if changed:
        print(f"Fixed:      {name}")
        total_fixed += 1
    else:
        print(f"No changes: {name}")

print(f"\nDone. Files modified: {total_fixed}/{len(html_files)}")
