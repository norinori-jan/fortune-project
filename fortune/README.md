# 易占い（周易）アプリ

八卦・六十四卦・変爻を使ったデジタル易占いアプリです。

## 新機能: 履歴保存と検証

- 占い実行時に SQLite へ自動保存
- 保存項目: 名前、質問、日時、本卦/之卦/変爻、Gemini回答、フィードバック
- 履歴一覧から後日フィードバックを更新し、占断と実際の差分を検証可能
- 一致度の自己評価スコア（1〜5）を記録可能
- 履歴検索（名前・期間・質問キーワード・スコア範囲）と CSV エクスポートに対応
- CSV は UTF-8 BOM 付きで出力し、Mac/Googleスプレッドシートで開きやすい形式
- CSV に AI回答の短縮要約列（ai_response_short）を追加
- 評価日時ベースの週次/月次トレンドAPIを追加
- GoogleスプレッドシートAPI連携でワンクリック自動転送に対応

## 前提

- Python 3.10+
- Node.js 20+

## はじめてのセットアップ

1. バックエンド依存を入れる

```bash
cd backend
pip install -r requirements.txt
```

2. フロントエンド依存を入れる

```bash
cd ../frontend
npm install
```

3. 環境変数ファイルを作る

```bash
cd /workspaces/fortune/backend
cp .env.example .env

cd /workspaces/fortune/frontend
cp .env.example .env
```

## 起動方法（推奨: 開発モード）

1. フロントエンド開発サーバーを起動

```bash
cd frontend
npm run dev
```

2. バックエンドを別ターミナルで起動

```bash
cd backend
python app.py
```

3. ブラウザで開く

- http://localhost:5000
- Codespaces の場合: https://glorious-space-pancake-x5rrprxrq9gvfp6v9-5000.app.github.dev

補足:
- frontend/dist が存在しない場合、バックエンドは FRONTEND_DEV_SERVER へ自動リダイレクトします。
- これで root の 404 再発を避けられます。

## 起動方法（本番ビルド確認）

```bash
cd frontend
npm run build

cd ../backend
python app.py
```

## 環境変数

### backend/.env

- PORT: Flask の待受ポート（既定 5000）
- FLASK_DEBUG: 1 でデバッグ有効
- FRONTEND_DEV_SERVER: dist 未生成時の転送先（既定 http://127.0.0.1:5173）
- DB_PATH: SQLite ファイルパス（既定 backend/divinations.db）

### frontend/.env

- VITE_API_BASE_URL: API のベース URL

例:
- 開発時（Vite proxy 利用）: 空文字のまま
- 静的配信や別ドメイン: http://localhost:5000

### github.dev / Codespaces での推奨値（この環境の具体値）

backend/.env:

```env
FRONTEND_DEV_SERVER=https://glorious-space-pancake-x5rrprxrq9gvfp6v9-5173.app.github.dev
PORT=5000
```

frontend/.env:

```env
VITE_API_BASE_URL=https://glorious-space-pancake-x5rrprxrq9gvfp6v9-5000.app.github.dev
```

補足:
- バックエンドは FRONTEND_DEV_SERVER が未設定でも、Codespaces の場合はアクセス元 URL から 5173 を自動推定します。

## テスト

```bash
cd backend
pytest -q
```

## API

| メソッド | パス | 説明 |
| --- | --- | --- |
| POST | /api/divine | 占いを実行し、本卦・変爻・之卦を返す |
| GET | /api/trigrams | 八卦の一覧を返す |
| GET | /api/health | ヘルスチェック |
| GET | /api/divinations | 保存済み占い履歴の一覧取得 |
| PATCH | /api/divinations/:id | フィードバック更新 |
| GET | /api/divinations/export.csv | 履歴のCSVエクスポート |
| GET | /api/divinations/stats/trend | 一致度推移（週次/月次） |
| GET | /api/divinations/stats/categories | カテゴリ別一致度比較 |
| POST | /api/divinations/export/sheets | Google Sheetsへ自動転送 |

### 履歴検索クエリ

GET /api/divinations と GET /api/divinations/export.csv では以下が使えます。

- person_name: 名前部分一致
- keyword: 質問文部分一致
- from_date: 開始日（YYYY-MM-DD）
- to_date: 終了日（YYYY-MM-DD）
- min_score: 最小自己評価スコア（1〜5）
- max_score: 最大自己評価スコア（1〜5）

trend API では `group=weekly` または `group=monthly` を指定してください。

`POST /api/divine` では `concern_type` を任意で渡せます。未指定時は質問文先頭の `【カテゴリ】` を自動解析します。

### CSV列（分析向け）

- id
- person_name
- category
- question
- created_at
- lower_number / upper_number / changing_line
- honke_meaning / shike_meaning
- hexagram_summary（卦の意味要約）
- honke_name / shike_name
- ai_response
- ai_response_short（AI回答の短縮要約）
- feedback
- self_score
- evaluated_at（評価日時）

### Googleスプレッドシート連携設定

backend/.env に以下を設定してください。

- GOOGLE_SHEETS_SPREADSHEET_ID: 転送先スプレッドシートID
- GOOGLE_SERVICE_ACCOUNT_FILE: Service Account JSONファイルのパス
	- もしくは GOOGLE_SERVICE_ACCOUNT_JSON に JSON文字列を直接設定
- GOOGLE_SHEETS_TAB_NAME: 転送先タブ名（省略時: Divinations）

注意:
- 転送先シートを Service Account のメールアドレスに共有しておく必要があります。
