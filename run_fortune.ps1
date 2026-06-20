# run_fortune.ps1
# fortune-project サーバー起動スクリプト
# 使い方: .\run_fortune.ps1

$ErrorActionPreference = "Stop"
$root = "C:\Users\norin\fortune-project"

Write-Host ""
Write-Host "🔮 fortune-project 起動中..." -ForegroundColor Cyan

# .env 確認
if (-not (Test-Path "$root\.env")) {
    Write-Host "⚠️  .env ファイルが見つかりません。" -ForegroundColor Yellow
    Write-Host "   以下を実行して作成してください："
    Write-Host '   @"ANTHROPIC_API_KEY=sk-ant-..." | Set-Content .env'
    exit 1
}

# 依存パッケージ確認
$deps = @("fastapi","uvicorn","anthropic","python-dotenv","pydantic")
foreach ($pkg in $deps) {
    $check = pip show $pkg 2>$null
    if (-not $check) {
        Write-Host "📦 $pkg をインストール中..." -ForegroundColor Yellow
        pip install $pkg -q
    }
}

Write-Host ""
Write-Host "✅ 起動します: http://localhost:8000" -ForegroundColor Green
Write-Host "   API ドキュメント: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "   停止: Ctrl+C" -ForegroundColor Gray
Write-Host ""

Set-Location $root
uvicorn server.app:app --reload --port 8000
