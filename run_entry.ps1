# 今日すぐ動かす：占いサーバーと「占いの入り口」を、この PC で起動して開きます（fortune-project のフォルダで実行）
& {
  $root = Split-Path -Parent $MyInvocation.MyCommand.Path
  if (-not $root) { $root = (Get-Location).Path }
  Set-Location $root
  $py = if (Get-Command py -ErrorAction SilentlyContinue) { 'py' } elseif (Get-Command python -ErrorAction SilentlyContinue) { 'python' } else { $null }
  if (-not $py) { Write-Host 'Python が見つかりません。'; return }
  & $py -m pip install --quiet fastapi "uvicorn[standard]" python-dotenv pydantic httpx
  Start-Process powershell -ArgumentList '-NoExit','-Command',"cd '$root'; $py -m uvicorn server.app:app --host 127.0.0.1 --port 8000"
  Start-Process powershell -ArgumentList '-NoExit','-Command',"cd '$root\apps\fortune-hub'; $py -m http.server 3000 --bind 127.0.0.1"
  Start-Sleep -Seconds 4
  Start-Process 'http://localhost:3000/entry.html?api=http://127.0.0.1:8000'
  Write-Host '開きました。終わるときは、開いた2つの黒い窓を閉じてください。'
}
