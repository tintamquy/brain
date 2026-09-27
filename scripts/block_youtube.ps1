# Script chặn YouTube Web và giữ lại studio.youtube.com
# Yêu cầu quyền Administrator

$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
$backupPath = "$env:SystemRoot\System32\drivers\etc\hosts.backup"

# 1. Tạo bản sao lưu dự phòng nếu chưa có
if (-not (Test-Path $backupPath)) {
    Copy-Item -Path $hostsPath -Destination $backupPath -Force
    Write-Host "[+] Da sao luu file hosts thanh cong: $backupPath" -ForegroundColor Green
}

# 2. Đọc nội dung hiện tại
$content = Get-Content -Path $hostsPath -Raw

$blockSignature = "# === Block YouTube Web (Allow Studio) ==="

if ($content -match [regex]::Escape($blockSignature)) {
    Write-Host "[!] Da co cau hinh chan YouTube trong file hosts roi." -ForegroundColor Yellow
} else {
    $rules = @"

$blockSignature
127.0.0.1 www.youtube.com
127.0.0.1 m.youtube.com
127.0.0.1 youtu.be
::1 www.youtube.com
::1 m.youtube.com
::1 youtu.be
# ========================================
"@
    Add-Content -Path $hostsPath -Value $rules -Encoding UTF8
    Write-Host "[+] Da them quy tac chan www.youtube.com vao file hosts." -ForegroundColor Green
}

# 3. Xóa cache DNS để áp dụng ngay lập tức
Clear-DnsClientCache
ipconfig /flushdns | Out-Null
Write-Host "[+] Da lam moi bo nho dem DNS (Flush DNS)." -ForegroundColor Green
Write-Host "[*] Hoan tat! Trang web www.youtube.com da bi chan, con studio.youtube.com van truy cap duoc binh thuong." -ForegroundColor Cyan
Start-Sleep -Seconds 3
