# fix_encoding.ps1
# Fixes UTF-8 characters that were mis-read as Latin-1 (mojibake) in all HTML files.

$htmlFiles = Get-ChildItem -Path $PSScriptRoot -Filter '*.html' | Select-Object -ExpandProperty FullName

# Each key is the broken byte sequence as it appears in the file (UTF-8 bytes interpreted as Windows-1252/Latin-1)
# Each value is the correct replacement string.
$replacements = [ordered]@{
    # --- Punctuation / currency ---
    "â€""    = [string][char]0x2013   # en dash  –
    "â€""    = [string][char]0x2014   # em dash  —
    "â€™"    = [string][char]0x2019   # right single quote  '
    "â€˜"    = [string][char]0x2018   # left single quote   '
    "â€œ"    = [string][char]0x201C   # left double quote   "
    "â€"     = [string][char]0x201D   # right double quote  "
    "â€¢"    = [string][char]0x2022   # bullet  •
    "â€¦"    = [string][char]0x2026   # ellipsis  …
    "Â·"     = [string][char]0x00B7   # middle dot  ·
    "Â°"     = [string][char]0x00B0   # degree  °
    "Â©"     = [string][char]0x00A9   # copyright  ©
    "Â®"     = [string][char]0x00AE   # registered  ®
    "Â£"     = [string][char]0x00A3   # pound  £
    "â‚¬"    = [string][char]0x20AC   # euro  €
    "Â½"     = [string][char]0x00BD   # 1/2  ½
    "Â"      = [string][char]0x00A0   # non-breaking space (lone Â)
    "â€¬"    = ""                      # invisible left-to-right mark – just remove

    # --- Arrows / symbols ---
    "â†'"    = [string][char]0x2192   # right arrow  →
    "â€º"    = [string][char]0x203A   # single right guillemet  ›
    "â"€"    = [string][char]0x2500   # box drawing light horizontal ─
    "âš½"    = "⚽"
    "âœ¦"    = "✦"
    "â­"     = "⭐"
    "â""     = "❓"
    "â†'"   = "→"

    # --- Multi-byte emoji (4-byte emojis mis-decoded) ---
    # Basketball
    "ðŸ€"    = "🏀"
    # Racing car (various broken forms)
    "ðŸ Žï¸ " = "🏎️"
    "ðŸ Žï¸"  = "🏎️"
    "ðŸŽï¸"   = "🏎️"
    # Boxing glove
    "ðŸ¥Š"    = "🥊"
    # Clapperboard
    "ðŸŽ¬"    = "🎬"
    # Performing arts
    "ðŸŽ­"    = "🎭"
    # Rocket
    "ðŸš€"    = "🚀"
    # Fire
    "ðŸ"¥"    = "🔥"
    # Laughing face
    "ðŸ˜‚"    = "😂"
    # TV
    "ðŸ"º"    = "📺"
    # Globe
    "ðŸŒ"     = "🌍"
    # Credit card
    "ðŸ'³"    = "💳"
    # Speech bubble
    "ðŸ'¬"    = "💬"
    # Trophy
    "ðŸ†"     = "🏆"
    # Gold medal
    "ðŸ¥‡"    = "🥇"
    # Stars
    "ðŸ'«"    = "💫"
    "ðŸŒŸ"    = "🌟"
    # Explosion
    "ðŸ'¥"    = "💥"
    # Lock
    "ðŸ"'"    = "🔒"
    # Soccer ball
    "âš½"     = "⚽"
    # Check mark entities (leave as-is but normalise)
    # Football / sport
    "ðŸŽ¯"    = "🎯"
}

$totalFixed = 0
foreach ($file in $htmlFiles) {
    $content = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)
    $original = $content
    foreach ($bad in $replacements.Keys) {
        $good = $replacements[$bad]
        $content = $content.Replace($bad, $good)
    }
    if ($content -ne $original) {
        [System.IO.File]::WriteAllText($file, $content, (New-Object System.Text.UTF8Encoding $false))
        Write-Host "Fixed: $file"
        $totalFixed++
    } else {
        Write-Host "No changes needed: $(Split-Path $file -Leaf)"
    }
}
Write-Host ""
Write-Host "Done. Files modified: $totalFixed"
