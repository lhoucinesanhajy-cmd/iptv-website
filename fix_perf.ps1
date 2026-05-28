# Performance fix: async Google Fonts + Font Awesome on all HTML pages
$rootPath = "c:\Users\admin\Desktop\iptv-website"
$files = Get-ChildItem -Path $rootPath -Recurse -Include "*.html" | Where-Object { $_.Name -ne "index.html" }

$asyncFonts = @"
<!-- Google Fonts: async non-blocking load -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;family=Poppins:wght@700;800;900&amp;display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;family=Poppins:wght@700;800;900&amp;display=swap"></noscript>
<!-- Font Awesome: async non-blocking load -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" media="print" onload="this.media='all'" crossorigin="anonymous" referrerpolicy="no-referrer">
<noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" crossorigin="anonymous"></noscript>
</head>
"@

foreach ($file in $files) {
    $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
    $original = $content
    $changed = $false

    # Check if already has async pattern
    if ($content -match 'media="print" onload') {
        Write-Host "SKIP (already async): $($file.Name)"
        continue
    }

    # Remove blocking Google Fonts link (at bottom of body or in head)
    $content = [regex]::Replace($content, '<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]*"[^>]*>', '')

    # Remove blocking Font Awesome link
    $content = [regex]::Replace($content, '<link rel="stylesheet" href="https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/6\.5\.2/css/all\.min\.css"[^>]*>', '')

    # Remove Clarity placeholder
    $content = [regex]::Replace($content, '<script defer src="https://www\.clarity\.ms/tag/YOUR_CLARITY_ID"></script>', '')

    # Inject async links before </head>
    if ($content -ne $original) {
        $content = $content -replace '</head>', $asyncFonts
        $changed = $true
    }

    if ($changed) {
        [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.UTF8Encoding]::new($false))
        Write-Host "Updated: $($file.Name)"
    } else {
        Write-Host "No changes: $($file.Name)"
    }
}

Write-Host "All done!"
