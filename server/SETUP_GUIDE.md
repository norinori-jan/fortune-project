# 🔮 タロット占いサーバー セットアップガイド

## 概要

このセットアップにより、ブラウザ（`index.html`）とPythonサーバーが連携し、APIキーをサーバー側で安全に管理してタロット占いを実行できます。

```
Browser (No API Keys)
    ↓ JSON request
    ↓
Flask Server (Port 5000)
    ├── /api/tarot/draw       (占い実行)
    ├── /api/tarot/interpret  (AI読み解き)
    └── registry_a.json に結果保存
```

---

## セットアップ手順

### 1. 環境変数ファイル設定

```bash
cd c:\Users\norin\fortune-project\server
cp .env.example .env
```

**`.env` ファイルを編集してAPIキーを設定：**

```env
# Gemini API キー（必須）
GEMINI_API_KEY=AIzaSy_YOUR_KEY_HERE

# OpenAI API キー（必須）
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
```

**APIキー取得方法：**

#### 🔑 Gemini API キー
1. https://console.cloud.google.com/apis/credentials にアクセス
2. 「+ 認証情報を作成」 → 「APIキー」
3. 生成されたキーをコピー
4. `.env` の `GEMINI_API_KEY` に貼り付け

#### 🔑 OpenAI API キー
1. https://platform.openai.com/api-keys にアクセス
2. 「+ Create new secret key」
3. 生成されたキーをコピー（1度だけ表示される）
4. `.env` の `OPENAI_API_KEY` に貼り付け

⚠️ **重要**
- `.env` には実APIキーが含まれます
- `.env` は **絶対に Git にコミットしない**（`.gitignore` で除外済み）
- `.env` をバージョン管理外の安全な場所で管理してください
- 定期的にAPIキーをローテーションしてください

---

### 2. Python依存関係インストール

```bash
cd c:\Users\norin\fortune-project\server
pip install -r requirements.txt
```

**出力例：**
```
Successfully installed Flask-3.0.0 flask-cors-4.0.0 python-dotenv-1.0.0 requests-2.31.0
```

---

### 3. Flaskサーバー起動

```bash
cd c:\Users\norin\fortune-project\server
python app.py
```

**正常起動時の出力：**
```
🔮 Tarot Fortune Server Starting...
📁 Registry path: c:\Users\norin\fortune-project\core\registry_a.json
📁 Tarot module path: c:\Users\norin\fortune-project\fortune-registry\tarot
🔑 API Keys configured: {'claude': 'configured', 'gemini': 'configured', 'openai': 'configured'}

✨ Server running on http://localhost:5000
   Use /health to check status
 * Running on http://0.0.0.0:5000
```

---

### 4. ブラウザでアクセス

別のターミナル/ウィンドウで：

```bash
# ローカル開発用サーバー起動（オプション - 簡易HTTPサーバーの場合）
cd c:\Users\norin\fortune-project\fortune-registry\tarot
python -m http.server 8080
```

その後、ブラウザで以下にアクセス：

- **タロット占いUI**: `http://localhost:8080/index.html`
- **サーバーヘルスチェック**: `http://localhost:5000/health`

---

## API エンドポイント

### 1. ヘルスチェック
```bash
curl http://localhost:5000/health
```

**レスポンス：**
```json
{
  "status": "ok",
  "timestamp": "2026-05-26T10:30:45.123456",
  "tarot_available": true
}
```

---

### 2. タロット占い実行
```bash
curl -X POST http://localhost:5000/api/tarot/draw \
  -H "Content-Type: application/json" \
  -d '{
    "spread_type": "one_oracle",
    "question": "今日の運勢は？"
  }'
```

**リクエストボディ：**
```json
{
  "spread_type": "one_oracle|three_card|yes_no|daily|celtic_mini",
  "question": "問いかけ（オプション）"
}
```

**レスポンス：**
```json
{
  "success": true,
  "data": {
    "type": "tarot_reading",
    "spread": "one_oracle",
    "cards": [...],
    "drawn_at": "2026-05-26T10:30:45...",
    "prompt_context": "..."
  }
}
```

---

### 3. AI読み解き
```bash
curl -X POST http://localhost:5000/api/tarot/interpret \
  -H "Content-Type: application/json" \
  -d '{
    "cards_context": "【スプレッド】ワンオラクル...",
    "ais": ["claude", "gemini", "openai"]
  }'
```

**リクエストボディ：**
```json
{
  "cards_context": "カードコンテキストテキスト",
  "ais": ["claude", "gemini", "openai"]
}
```

**レスポンス：**
```json
{
  "success": true,
  "interpretations": {
    "claude": {
      "success": true,
      "text": "Claude の解読結果..."
    },
    "gemini": {
      "success": true,
      "text": "Gemini の解読結果..."
    },
    "openai": {
      "success": false,
      "text": "エラーメッセージ"
    }
  }
}
```

---

### 4. 過去の占い履歴取得
```bash
curl http://localhost:5000/api/registry/tarot
```

**レスポンス：**
```json
{
  "success": true,
  "count": 5,
  "entries": [
    {
      "type": "tarot_reading",
      "spread": "one_oracle",
      "cards": [...],
      "drawn_at": "..."
    },
    ...
  ]
}
```

---

### 5. サーバー設定確認
```bash
curl http://localhost:5000/api/config
```

**レスポンス：**
```json
{
  "api_keys": {
    "claude": "configured",
    "gemini": "configured",
    "openai": "configured"
  },
  "registry_file": "c:\\Users\\norin\\fortune-project\\core\\registry_a.json",
  "tarot_registry_path": "c:\\Users\\norin\\fortune-project\\fortune-registry\\tarot"
}
```

---

## ブラウザ操作フロー

1. **スプレッド選択** → 「一枚引き」「スリーカード」など
2. **質問入力** （オプション）
3. **✦ SHUFFLE ✦** ボタンをクリック
   - サーバーが `POST /api/tarot/draw` を実行
   - 占い結果を `registry_a.json` に保存
   - 結果をブラウザに返す
4. **カードをクリック** → 順に開く
5. **✦ 3つのAIで読み解く ✦** ボタン
   - サーバーが `POST /api/tarot/interpret` を実行
   - Claude / Gemini / OpenAI に並列リクエスト
   - 各AI の読み解き結果を表示

---

## トラブルシューティング

### ✗ `ConnectionRefusedError: Cannot connect to localhost:5000`

**解決策：**
1. Flaskサーバーが起動しているか確認
2. `python app.py` で起動
3. ポート5000がブロックされていないか確認

```bash
# ポート確認
netstat -ano | findstr :5000
```

---

### ✗ `ModuleNotFoundError: No module named 'tarot_engine'`

**解決策：**
1. `major.json` が `fortune-registry/tarot/` に存在するか確認
2. `tarot_engine.py` が同じディレクトリにあるか確認

```bash
# ファイル確認
dir c:\Users\norin\fortune-project\fortune-registry\tarot\
```

---

### ✗ `Claude API Error: 401`

**解決策：**
1. `.env` の `CLAUDE_API_KEY` が正しいか確認
2. APIキーがアクティブか確認（有効期限切れ等）
3. サーバーを再起動

```bash
# .env 確認
type .env | findstr CLAUDE_API_KEY
```

---

### ✗ ブラウザで占い実行後エラー

**ブラウザコンソール確認：**
1. F12 キーで開発者ツールを開く
2. Console タブでエラーメッセージを確認
3. Network タブで API呼び出しを確認（ステータスコード200か確認）

---

## ファイル構成

```
fortune-project/
├── server/
│   ├── app.py              ← Flask アプリケーション
│   ├── requirements.txt    ← Python依存関係
│   ├── .env                ← APIキー設定（Git無視）
│   └── .env.example        ← APIキーテンプレート
├── fortune-registry/tarot/
│   ├── index.html          ← 改修されたブラウザUI
│   ├── tarot_engine.py     ← タロットロジック
│   ├── tarot_registry_bridge.py
│   └── major.json          ← タロットカード定義
└── core/
    └── registry_a.json     ← 占い履歴保存先
```

---

## セキュリティ注意事項

✅ **このセットアップで実現：**
- APIキーがブラウザに露出しない
- サーバー側で安全に管理
- HTTPS対応可能（本番環境）

⚠️ **本番環境での注意：**
- `.env` を絶対に Git リポジトリに追加しない（`.gitignore` に記載済み）
- HTTPS/SSL/TLS の設定
- CORS設定の見直し（現在は全許可）
- 認証・認可の実装検討

🔐 **APIキーのセキュリティ**
1. `.env.example` には実キーを入れない（テンプレートのみ）
2. `.env` は `.gitignore` に含まれているため Git にコミットされない
3. ローカル開発時：`.env` をローカルマシンのみに保持
4. 本番環境：環境変数またはシークレット管理サービス（Azure Key Vault など）を使用

---

## 🎯 nori流 タロット鑑定スタイル

このサーバーは以下の鑑定スタイルに対応しています：

### 【読み解きの原則】
1. **4層構造で読む**：心理・状況・流れ・アドバイス
2. **エネルギーの方向性**：正位置/逆位置を吉凶ではなく流れとして扱う
3. **可能性提示**：未来を断定せず、選択肢を提示
4. **象徴から導く**：質問者の状況を想像しすぎず、カードの象徴から導く
5. **行動アドバイス**：最後に必ず1つの行動ヒントを提示

### 【出力フォーマット】
- カードの象徴
- 今の状況の読み解き
- 心理的背景
- これからの流れ
- 行動アドバイス（1つ）

### 【読み解きの特徴】
- 3〜6文で簡潔にまとめる
- 不安を煽らない
- 断定的な未来予言をしない
- 医療・法律の判断をしない
- 詩的かつ親しみやすい文体

---

## 使用技術

- **Backend**: Flask 3.0.0 (Python)
- **Frontend**: Vanilla JavaScript (API互換)
- **AI Models**: 
  - Gemini 1.5 Flash (Google)
  - GPT-4o (OpenAI)
- **Storage**: registry_a.json (JSON)

---

## 次のステップ

1. ✅ ローカル環境で動作確認
2. 🔄 HTTPS対応（本番環境）
3. 🔐 認証・認可実装
4. 📱 モバイルアプリ化
5. ☁️ クラウド展開（Azure など）

---

**質問・バグ報告**: issue を作成してください！

