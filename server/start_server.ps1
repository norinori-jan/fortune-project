# Tarot Fortune Server Startup Script
# ====================================
# 使い方: .\start_server.ps1

Write-Host "🔮 Tarot Fortune Server セットアップ" -ForegroundColor Cyan

$serverDir = Split-Path -Path $MyInvocation.MyCommand.Definition
$projectRoot = Split-Path -Path $serverDir
$envFile = Join-Path $serverDir ".env"
$envExample = Join-Path $serverDir ".env.example"

# ========================================
# Step 1: Check .env existence
# ========================================

if (-not (Test-Path $envFile)) {
    Write-Host "⚠️  .env ファイルが見つかりません" -ForegroundColor Yellow
    if (Test-Path $envExample) {
        Write-Host "💡 .env.example からコピーしています..." -ForegroundColor Cyan
        Copy-Item $envExample $envFile
        Write-Host "✓ .env を作成しました" -ForegroundColor Green
        Write-Host ""
        Write-Host "📝 .env ファイルを編集してAPIキーを設定してください:" -ForegroundColor Yellow
        Write-Host "   $envFile" -ForegroundColor White
        Write-Host ""
        Write-Host "その後、このスクリプトを再実行してください"
        exit 1
    } else {
        Write-Host "❌ .env.example もありません" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✓ .env ファイルが存在します" -ForegroundColor Green

# ========================================
# Step 2: Check Python
# ========================================

Write-Host ""
Write-Host "Python バージョン確認..." -ForegroundColor Cyan

try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python がインストールされていません" -ForegroundColor Red
    Write-Host "   https://www.python.org/ からインストールしてください" -ForegroundColor Yellow
    exit 1
}

# ========================================
# Step 3: Check pip dependencies
# ========================================

Write-Host ""
Write-Host "依存パッケージ確認..." -ForegroundColor Cyan

$requirements = @("flask", "flask-cors", "requests", "python-dotenv")
$missing = @()

foreach ($req in $requirements) {
    try {
        python -c "import ${req.replace('-', '_')}" 2>$null
        Write-Host "✓ $req" -ForegroundColor Green
    } catch {
        $missing += $req
        Write-Host "✗ $req (未インストール)" -ForegroundColor Red
    }
}

if ($missing.Count -gt 0) {
    Write-Host ""
    Write-Host "📦 不足しているパッケージをインストール中..." -ForegroundColor Cyan
    Set-Location $serverDir
    python -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ インストール失敗" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ インストール完了" -ForegroundColor Green
}

# ========================================
# Step 4: Check registry path
# ========================================

Write-Host ""
Write-Host "レジストリパス確認..." -ForegroundColor Cyan

$registryPath = Join-Path $projectRoot "core" "registry_a.json"
$tarotPath = Join-Path $projectRoot "fortune-registry" "tarot"

if (-not (Test-Path $tarotPath)) {
    Write-Host "❌ $tarotPath が見つかりません" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Tarot モジュール: $tarotPath" -ForegroundColor Green
Write-Host "✓ Registry 保存先: $registryPath" -ForegroundColor Green

# ========================================
# Step 5: Show API key status
# ========================================

Write-Host ""
Write-Host "API キー設定確認..." -ForegroundColor Cyan

$envContent = Get-Content $envFile | Select-String "^[A-Z_].*=.*"

foreach ($line in $envContent) {
    if ($line -match "^([A-Z_]+)=(.*)$") {
        $key = $matches[1]
        $value = $matches[2]
        if ($value -and $value -ne "" -and $value -notmatch "^\s*$") {
            Write-Host "✓ $key: 設定済み" -ForegroundColor Green
        } else {
            Write-Host "⚠️  $key: 未設定" -ForegroundColor Yellow
        }
    }
}

# ========================================
# Step 6: Start server
# ========================================

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "🚀 Flask サーバーを起動しています..." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 サーバーURL: http://localhost:5000" -ForegroundColor Yellow
Write-Host "📍 ヘルスチェック: http://localhost:5000/health" -ForegroundColor Yellow
Write-Host ""
Write-Host "⌨️  Ctrl+C で停止します" -ForegroundColor Cyan
Write-Host ""

Set-Location $serverDir

# Load .env into environment
$envContent = Get-Content $envFile
foreach ($line in $envContent) {
    if ($line -and -not $line.StartsWith("#")) {
        if ($line -match "^([A-Z_]+)=(.*)$") {
            $key = $matches[1]
            $value = $matches[2]
            Set-Item "env:$key" $value
        }
    }
}

# Start server
python app.py

Write-Host ""
Write-Host "⏹️  サーバーを停止しました" -ForegroundColor Yellow
