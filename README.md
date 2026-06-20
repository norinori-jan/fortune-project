# 🔮 fortune-project

> 易・タロット・風水・四柱推命を「一つの思想体系の異なる表現」として統合した占術プラットフォーム

---

## 概要

| ツール | 認識の軸 | 問いの形式 |
|-------|---------|-----------|
| 易（梅花心易） | 時間軸・変化の流れ | 「この流れはどう変化するか」 |
| タロット | 象徴と心理の投影 | 「今の状況の本質は何か」 |
| 羅盤（風水） | 空間軸・地気の配置 | 「この場所のエネルギーはどうか」 |
| 四柱推命 | 時間の気質 | 「今という時間はどんな性格か」 |

これらは**同一の「問い」を異なる次元で照らすレンズ**です。

---

## セットアップ

### 1. リポジトリのクローン（初回のみ）

```powershell
cd C:\Users\norin
git clone https://github.com/norinori-jan/fortune-project.git
cd fortune-project
```

### 2. 環境変数の設定

```powershell
# .env ファイルを作成
@"
ANTHROPIC_API_KEY=sk-ant-ここにキーを貼る
"@ | Set-Content .env -Encoding UTF8
```

### 3. Python依存パッケージのインストール

```powershell
pip install fastapi uvicorn anthropic python-dotenv pydantic
```

### 4. サーバー起動

```powershell
cd C:\Users\norin\fortune-project
uvicorn server.app:app --reload --port 8000
```

ブラウザで http://localhost:8000/docs を開くと Swagger UI が表示されます。

---

## クイックスタート

### 易で占う（PowerShell）

```powershell
Invoke-RestMethod -Uri http://localhost:8000/fortune/run `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"tool":"iching","question":"転職の時期はいつが良いですか"}'
```

### タロットで占う

```powershell
Invoke-RestMethod -Uri http://localhost:8000/fortune/run `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"tool":"tarot","question":"今の恋愛の行方を教えてください"}'
```

### AI読み解きを生成する

```powershell
# Step1: 占術実行
$result = Invoke-RestMethod -Uri http://localhost:8000/fortune/run `
  -Method POST -ContentType "application/json" `
  -Body '{"tool":"iching","question":"新しいビジネスを始めるべきか"}'

# Step2: AI読み解き
$body = @{
  tool       = "iching"
  question   = "新しいビジネスを始めるべきか"
  raw_result = $result.raw_result
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/fortune/query `
  -Method POST -ContentType "application/json" -Body $body
```

---

## registry_a.json の更新

データを更新したい場合：

```powershell
cd C:\Users\norin\fortune-project\core
python registry_a.py
```

`core/registry_a.json` が再生成されます。変更後は `fortune-core` にも push してください：

```powershell
cd C:\Users\norin\_migration_work\fortune-core
Copy-Item C:\Users\norin\fortune-project\core\registry_a.json .\
git add registry_a.json
git commit -m "update: registry_a.json"
git push origin main
```

---

## プロジェクト構造

詳細は [docs/PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md) を参照してください。

```
fortune-project/
├── core/shared/      ← 全アプリ共通（cosmology.js, reading.js, ui-tokens.css）
├── server/app.py     ← FastAPI エンドポイント
├── fortune-core/     ← 梅花心易・タロットエンジン
├── fortune-registry/ ← プロンプト・カードデータ
├── fenshui_map/      ← 風水マップ（React+Firebase）
└── docs/             ← ドキュメント
```

---

## GitHub Pages

`fortune-core` リポジトリの GitHub Pages で registry_a.json を配信中：

```
https://norinori-jan.github.io/fortune-core/registry_a.json
```

---

## ライセンス

Private Repository — norinori-jan
