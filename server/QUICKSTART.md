# 🔮 ローカルフラスク サーバー　セットアップガイド

## 📋 5分で完成！

### 1️⃣ APIキー設定（1分）

```powershell
cd c:\Users\norin\fortune-project\server
cp .env.example .env
```

`.env` ファイルを編集して、以下を入力：

```env
# Gemini API キー
GEMINI_API_KEY=AIzaSy_YOUR_KEY_HERE

# OpenAI API キー
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
```

**キー取得方法：**
- **Gemini**: https://console.cloud.google.com/apis/credentials
- **OpenAI**: https://platform.openai.com/api-keys

---

### 2️⃣ Python依存関係インストール（1分）

```powershell
cd c:\Users\norin\fortune-project\server
pip install -r requirements.txt
```

**出力例：**
```
Successfully installed Flask-3.0.0 flask-cors-4.0.0 python-dotenv-1.0.0 requests-2.31.0
```

---

### 3️⃣ Flaskサーバー起動（1分）

**方法A: スクリプト使用（推奨）**
```powershell
cd c:\Users\norin\fortune-project\server
.\start_server.ps1
```

**方法B: 手動起動**
```powershell
cd c:\Users\norin\fortune-project\server
python app.py
```

**成功時の表示：**
```
🔮 Tarot Fortune Server Starting...
📁 Registry path: c:\Users\norin\fortune-project\core\registry_a.json
📁 Tarot module path: c:\Users\norin\fortune-project\fortune-registry\tarot
🔑 API Keys configured: {'claude': 'not configured', 'gemini': 'configured', 'openai': 'configured'}

✨ Server running on http://localhost:5000
   Use /health to check status
 * Running on http://0.0.0.0:5000/
```

---

### 4️⃣ ブラウザ起動（1分）

別ウィンドウで：

```powershell
cd c:\Users\norin\fortune-project\fortune-registry\tarot
python -m http.server 8080
```

ブラウザで開く：
```
http://localhost:8080/index.html
```

---

### 5️⃣ 占いを実行（2分）

1. **スプレッド選択** → 「一枚引き」など
2. **質問入力** （オプション）
3. **✦ SHUFFLE ✦** クリック
4. **カードをクリック** → 開く
5. **✦ 3つのAIで読み解く ✦** クリック

✨ **複数のAIの解読が同時表示されます！**

---

## 🔍 動作確認

### ヘルスチェック
```bash
curl http://localhost:5000/health
```

### 占い実行テスト
```bash
curl -X POST http://localhost:5000/api/tarot/draw \
  -H "Content-Type: application/json" \
  -d '{\"spread_type\": \"one_oracle\", \"question\": \"今日の運勢は？\"}'
```

---

## ⚠️ よくあるエラー

| エラー | 原因 | 解決策 |
|------|------|------|
| `Connection refused` | サーバーが起動していない | `python app.py` で起動 |
| `ModuleNotFoundError` | パッケージ未インストール | `pip install -r requirements.txt` |
| `401 Unauthorized` | APIキーが間違っている | `.env` を再確認 |
| CORS エラー | ブラウザからアクセス不可 | サーバーが起動しているか確認 |

---

## 📂 ファイル構成

```
fortune-project/
├── server/
│   ├── app.py              ← メインサーバー
│   ├── requirements.txt
│   ├── .env                ← APIキー（作成必須・Git無視）
│   ├── .env.example        ← テンプレート
│   ├── start_server.ps1    ← 起動スクリプト
│   └── SETUP_GUIDE.md      ← 詳細ガイド
├── fortune-registry/tarot/
│   ├── index.html          ← ブラウザUI
│   ├── tarot_engine.py     ← タロットロジック
│   └── major.json          ← タロットカード定義
└── core/
    └── registry_a.json     ← 占い履歴保存先
```

---

## 🚀 次のステップ

- ✅ ローカルで動作確認
- 📖 [詳細セットアップガイド](./SETUP_GUIDE.md) を参照
- ☁️ 本番環境への展開（Azure Functions など）
- 🔐 HTTPS/認証設定

---

**Happy Tarot Reading! 🔮**
