$ProjectDir = "C:\Users\norin\fortune-project"
$DownloadDir = "$env:USERPROFILE\Downloads"
Set-Location $ProjectDir
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Fortune Project 起動" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[1/3] tarot engine.py を実行中..." -ForegroundColor Yellow
python "$DownloadDir\tarot engine.py"
if ($LASTEXITCODE -ne 0) { Write-Host "  エラー" -ForegroundColor Red } else { Write-Host "  完了" -ForegroundColor Green }
Write-Host ""
Write-Host "[2/3] tarot registry bridge.py を実行中..." -ForegroundColor Yellow
python "$DownloadDir\tarot registry bridge.py"
if ($LASTEXITCODE -ne 0) { Write-Host "  エラー" -ForegroundColor Red } else { Write-Host "  完了" -ForegroundColor Green }
Write-Host ""
Write-Host "[3/3] engine patch.py を実行中..." -ForegroundColor Yellow
python "$DownloadDir\engine patch.py"
if ($LASTEXITCODE -ne 0) { Write-Host "  エラー" -ForegroundColor Red } else { Write-Host "  完了" -ForegroundColor Green }
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  すべて完了しました" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
