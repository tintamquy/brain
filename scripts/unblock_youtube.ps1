# Script gỡ chặn YouTube
# Yêu cầu quyền Administrator

$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"

if (Test-Path $hostsPath) {
    $lines = Get-Content -Path $hostsPath
    $filtered = $lines | Where-Object {
        $_ -notmatch "www\.youtube\.com" -and
        $_ -notmatch "m\.youtube\.com" -and
        $_ -notmatch "youtu\.be" -and
        $_ -notmatch "Block YouTube Web" -and
        $_ -notmatch "======"
    }
    Set-Content -Path $hostsPath -Value $filtered -Encoding UTF8
    Clear-DnsClientCache
    ipconfig /flushdns | Out-Null
    Write-Host "[+] Da go chan YouTube thanh cong!" -ForegroundColor Green
    Start-Sleep -Seconds 3
}
