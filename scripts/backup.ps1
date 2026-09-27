# Obsidian Vault Auto-Backup Script
$VaultPath = "D:\Projects\SecondBrain"
Set-Location -Path $VaultPath

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "[$timestamp] Checking for changes in $VaultPath..." -ForegroundColor Cyan

# Fetch remote
git fetch origin main 2>$null

# Check local changes
$status = git status --porcelain

if ($status) {
    Write-Host "[$timestamp] Changes detected. Committing and pushing..." -ForegroundColor Yellow
    git add -A
    git commit -m "auto sync $timestamp window"
    git pull --rebase origin main
    git push origin main
    Write-Host "[$timestamp] Backup completed successfully!" -ForegroundColor Green
} else {
    Write-Host "[$timestamp] No local changes detected." -ForegroundColor Green
}
