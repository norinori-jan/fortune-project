# 🔮 fortune-project — PROJECT SUMMARY

> タロット占いサーバー＋AIによる鑑定アプリ。Flask（Python）をバックエンドに、複数のAIプロバイダー（Gemini / OpenAI / Claude）で鑑定文を生成する。

---

## 1. プロジェクト概要

| 項目 | 内容 |
|------|------|
| 目的 | タロットカードをドローし、AIがnori流スタイルで鑑定文を生成する |
| バックエンド | Flask（Python）— APIキー管理・占い実行・AI解釈 |
| フロントエンド | HTML/JS（tarot_engine.py + index.html）— iPhone / PCブラウザで動作 |
| データ | JSON形式（major.json, registry_a.json）—カード情報・履歴管理 |
| AI | Gemini 1.5 Flash（主）/ OpenAI GPT-4o（副）/ Claude（予定） |

---

## 2. ディレクトリ構成

```
fortune-project/
├── PROJECT_SUMMARY.md        ← このファイル（総括）
│
├── server/                   ← Flaskバックエンド
│   ├── app.py                ← メインサーバー（APIエンドポイント・AI呼び出し）
│   ├── .env                  ← 実APIキー（Git管理外・自分で作成）
│   ├── .env.example          ← キーのテンプレート（値なし）
│   ├── QUICKSTART.md         ← 5分セットアップガイド
│   └── SETUP_GUIDE.md        ← 詳細ガイド＋nori流鑑定スタイル
│
├── core/
│   └── registry_a.json       ← 鑑定履歴・ユーザーデータのJSONストア
│
└── fortune-registry/tarot/
    ├── index.html            ← タロットUI（ブラウザで動作）
    ├── tarot_engine.py       ← カードドロー・シャッフルロジック
    └── major.json            ← 大アルカナ22枚のデータ
```

---

## 3. Flaskサーバーの役割（app.py）

```
[iPhone/PC ブラウザ]
        ↓ HTTP リクエスト
[Flask サーバー :5000]
        ↓
  ┌─────────────────┐
  │ APIキー管理      │ ← .env から安全に読み込み
  │ カードドロー     │ ← major.json からランダム抽選
  │ AI解釈生成      │ ← Gemini / OpenAI に送信
  │ 履歴保存        │ ← registry_a.json に書き込み
  └─────────────────┘
```

- APIキーはサーバー側のみで保持（フロントエンドに露出しない）
- AI呼び出しに失敗した場合は自動でフォールバック

---

## 4. APIキーの管理方法

### .env.example（テンプレート。値は空欄のまま）

```env
# AI Provider Keys
GEMINI_API_KEY=
OPENAI_API_KEY=

# Flask Settings
FLASK_ENV=development
SECRET_KEY=
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:5500

# Claude（未統合・将来用）
# ANTHROPIC_API_KEY=
```

### .env（自分で作成。Gitにコミットしない）

```powershell
cd C:\Users\norin\fortune-project\server
copy .env.example .env
# → .env を開いて実際のキーを入力
```

### セキュリティルール

| 項目 | 対応 |
|------|------|
| `.env` をGitに入れない | `.gitignore` に記載済み |
| `.env.example` に実キーを書かない | テンプレートのみ |
| フロントから直接API呼び出しをしない | Flaskサーバー経由のみ |
| キーのローテーション | 3ヶ月ごと推奨 |

---

## 5. 使用AI と切り替え仕様

| AI | モデル | 状態 | 用途 |
|----|--------|------|------|
| Gemini | gemini-1.5-flash | ✅ 統合済み | 主力（無料枠あり） |
| OpenAI | gpt-4o | ✅ 統合済み | バックアップ |
| Claude | claude-3-haiku | 🔜 予定 | 将来の選択肢 |

**切り替え方法（app.py内）:**

```python
AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini")  # "gemini" or "openai"
```

`.env` に `AI_PROVIDER=openai` と書くだけで切り替え可能。

---

## 6. nori流タロット鑑定スタイル（system prompt）

```
あなたはnoriという名のタロット占い師です。

【鑑定の4層構造】
1. 心理層   — カードが映す相談者の内面・潜在意識
2. 状況層   — 現在の外部環境・人間関係・流れ
3. 流れ層   — 過去→現在→未来のエネルギーの変化
4. アドバイス層 — 具体的な行動・視点の転換

【表現のルール】
- 断言しない。可能性と選択肢を提示する
- 「〜かもしれません」「〜という流れが見えます」
- 共感を先に置く。批判・脅しは絶対にしない
- 逆位置は「否定」ではなく「見直すサイン」として解釈
- 最後は必ず希望・行動へのエンパワーメントで締める
```

---

## 7. APIエンドポイント一覧

| メソッド | エンドポイント | 説明 |
|----------|---------------|------|
| GET | `/health` | サーバー生存確認 |
| GET | `/api/config` | AI設定・バージョン確認 |
| POST | `/api/tarot/draw` | カードをドロー（枚数指定可） |
| POST | `/api/tarot/interpret` | ドローしたカードをAIが鑑定 |
| GET | `/api/registry/tarot` | 鑑定履歴の取得 |
| POST | `/api/registry/tarot` | 鑑定結果を保存 |

### リクエスト例

```bash
# ヘルスチェック
curl http://localhost:5000/health

# カードを3枚ドロー
curl -X POST http://localhost:5000/api/tarot/draw \
  -H "Content-Type: application/json" \
  -d '{"count": 3}'

# AI鑑定
curl -X POST http://localhost:5000/api/tarot/interpret \
  -H "Content-Type: application/json" \
  -d '{"cards": ["The Fool", "The Tower"], "question": "転職すべきか"}'
```

---

## 8. セットアップ手順（QUICKSTART要約）

```powershell
# 1. リポジトリに移動
cd C:\Users\norin\fortune-project\server

# 2. 仮想環境を作成・有効化
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. 依存パッケージをインストール
pip install flask flask-cors python-dotenv google-generativeai openai

# 4. .env を作成してAPIキーを入力
copy .env.example .env
notepad .env

# 5. サーバー起動
python app.py
```

ブラウザで `http://localhost:5000/health` を開いて `{"status": "ok"}` が返れば成功。

### iPhoneから接続する場合

```powershell
# PCのIPアドレスを確認
ipconfig
# → 例: 192.168.1.5

# app.py を以下で起動（0.0.0.0 = 全デバイスからアクセス可）
flask run --host=0.0.0.0 --port=5000
```

iPhoneのSafariで `http://192.168.1.5:5000` にアクセス（同じWi-Fi必須）。

---

## 9. トラブルシューティング

| 症状 | 原因 | 対処 |
|------|------|------|
| `ModuleNotFoundError` | 仮想環境が有効でない | `.\venv\Scripts\Activate.ps1` を実行 |
| `401 Unauthorized` | APIキーが無効・未設定 | `.env` のキーを確認・再生成 |
| iPhoneから繋がらない | ホストが `127.0.0.1` のまま | `--host=0.0.0.0` で起動 |
| CORSエラー | `ALLOWED_ORIGINS` 未設定 | `.env` にフロントのURLを追加 |
| Gemini失敗→無応答 | フォールバック未設定 | `AI_PROVIDER=openai` に切り替え |

---

## 10. 今後の拡張

### HTTPS化（ローカル）

```powershell
pip install pyopenssl
flask run --host=0.0.0.0 --port=5000 --cert=adhoc
```

### 本番環境

| 項目 | 推奨 |
|------|------|
| ホスティング | Azure App Service / Render / Railway |
| APIキー管理 | Azure Key Vault / Railway Secrets |
| HTTPS | Let's Encrypt（自動） |
| 認証 | Firebase Auth / JWT |
| DB | SQLite → PostgreSQL へ移行 |

### Claude統合（将来）

```python
# app.py に追加予定
import anthropic
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
```

---

*最終更新: 2026-06-06 | nori fortune-project v1.0*
