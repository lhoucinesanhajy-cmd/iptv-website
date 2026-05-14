$path = "c:\Users\admin\Desktop\iptv-website"
$files = Get-ChildItem -Path $path -Filter "*.html" -Recurse

foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw
    $pattern = "(?s)<!-- Microsoft Clarity -->\s*<script type=`"text/javascript`">\s*\(function\(c,l,a,r,i,t,y\)\{.*?\n\s*\}\)\(window, document, `"clarity`", `"script`", `".*?`"\);\s*</script>\s*"
    
    if ($content -match $pattern) {
        $content = $content -replace $pattern, ""
        Set-Content -Path $file.FullName -Value $content
        Write-Host "Updated $($file.FullName)"
    }
}
