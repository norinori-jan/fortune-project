# 🔮 ローカルフラスク サーバー　クイックスタート

## 📋 5分で完成！

### 1️⃣ APIキー設定（1分）

```powershell
cd c:\Users\norin\fortune-project\server
cp .env.example .env
```

`.env` ファイルを編集して、以下を入力：

```env
CLAUDE_API_KEY=sk-ant-api03-YOUR_KEY_HERE
GEMINI_API_KEY=AIzaSy_YOUR_KEY_HERE
OPENAI_API_KEY=sk-YOUR_KEY_HERE
```

**キー取得方法：**
- Claude: https://console.anthropic.com/
- Gemini: https://makersuite.google.com/app/apikey
- OpenAI: https://platform.openai.com/api-keys

---

### 2️⃣ サーバー起動（1分）

**方法A: スクリプト使用（推奨）**
```powershell
cd c:\Users\norin\fortune-project\server
.\start_server.ps1
```

**方法B: 手動起動**
```powershell
cd c:\Users\norin\fortune-project\server
pip install -r requirements.txt  # 初回のみ
python app.py
```

**成功時の表示：**
```
✨ Server running on http://localhost:5000
   Use /health to check status
```

---

### 3️⃣ ブラウザ起動（1分）

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

### 4️⃣ 占いを実行（2分）

1. **スプレッド選択** → 「一枚引き」など
2. **質問入力** （オプション）
3. **✦ SHUFFLE ✦** クリック
4. **カードをクリック** → 開く
5. **✦ 3つのAIで読み解く ✦** クリック

✨ **3つのAIの解読が同時表示されます！**

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
  -d '{"spread_type": "one_oracle", "question": "今日の運勢は？"}'
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
│   ├── .env                ← APIキー（作成必須）
│   ├── .env.example        ← テンプレート
│   ├── start_server.ps1    ← 起動スクリプト
│   └── SETUP_GUIDE.md      ← 詳細ガイド
├── fortune-registry/tarot/
│   ├── index.html          ← ブラウザUI（改修済み）
│   ├── tarot_engine.py
│   └── major.json
└── core/
    └── registry_a.json     ← 占い履歴
```

---

## 🚀 次のステップ

- ✅ ローカルで動作確認
- 📖 [詳細セットアップガイド](./SETUP_GUIDE.md) を参照
- ☁️ 本番環境への展開（Azure Functions など）
- 🔐 HTTPS/認証設定

---

**Happy Tarot Reading! 🔮**
