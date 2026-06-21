# fortune-project

> 易・タロット・風水・四柱推命を「一つの思想体系の異なる表現」として統合した占術プラットフォーム  
> Claude / Gemini / OpenAI のマルチAIモデルに対応

---

## 🌐 公開URL

| サービス | URL |
|---------|-----|
| **fortune-project API** | https://fortune-project-api.onrender.com |
| **API ドキュメント** | https://fortune-project-api.onrender.com/docs |
| **fortune-hub UI** | `apps/fortune-hub/index.html` |
| **registry_a.json (CDN)** | https://norinori-jan.github.io/fortune-core/registry_a.json |

---

## 🔮 概要

| ツール | 認識の軸 | 問いの形式 |
|-------|---------|-----------|
| 易（梅花心易） | 時間軸・変化の流れ | 「この流れはどう変化するか」 |
| タロット | 象徴と心理の投影 | 「今の状況の本質は何か」 |
| 羅盤（風水） | 空間軸・地気の配置 | 「この場所のエネルギーはどうか」 |
| 四柱推命 | 時間の気質 | 「今という時間はどんな性格か」 |

---

## 🏗️ リポジトリ構造

```
fortune-project/
├── core/
│   ├── registry_a.json      ← SSOT（64卦・タロット・八卦・羅盤）
│   ├── registry_a.py        ← JSON生成スクリプト
│   └── shared/
│       ├── cosmology.js     ← 八卦・五行・十二支 共通型
│       ├── timeAxis.js      ← 干支・九星・梅花心易 時間計算
│       ├── reading.js       ← DivinationReading型・ReadingBridge
│       └── ui-tokens.css    ← 全UI共通デザイントークン
│
├── server/
│   └── app.py               ← FastAPI（Claude / Gemini / OpenAI 対応）
│
├── apps/
│   └── fortune-hub/
│       └── index.html       ← 統合ハブUI（五行レーダーチャート）
│
├── fortune-core/src/
│   ├── meihua/              ← 梅花心易エンジン（JS）
│   └── fortune_core/        ← Python占術ライブラリ
│
├── fortune-registry/
│   ├── prompts/             ← Claude / Gemini / OpenAI プロンプト
│   └── tarot/card_notes/    ← 大アルカナ22枚個別JSON
│
├── requirements.txt
├── render.yaml              ← Render デプロイ設定
└── run_fortune.ps1          ← ローカル起動スクリプト
```

---

## 🚀 セットアップ

### ローカル起動

```powershell
# 1. 環境変数設定
@"
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
OPENAI_API_KEY=sk-...
"@ | Set-Content .env -Encoding UTF8

# 2. 依存パッケージ
pip install -r requirements.txt

# 3. 起動
.\run_fortune.ps1
# または
uvicorn server.app:app --reload --port 8000
```

### registry_a.json 再生成

```powershell
cd core
python registry_a.py
```

---

## 📡 API 仕様

### `GET /fortune/health`

```json
{
  "status": "ok",
  "version": "2.1.0",
  "tools": ["iching", "meihua", "tarot", "shichu", "lopan"],
  "ai_models": { "claude": true, "gemini": true, "openai": true }
}
```

### `POST /fortune/run`

```json
{
  "tool": "iching",
  "question": "転職のタイミングはいつが良いですか"
}
```

### `POST /fortune/query`

```json
{
  "tool": "iching",
  "question": "転職のタイミングはいつが良いですか",
  "raw_result": { ... },
  "ai_model": "claude"
}
```

`ai_model` は `claude` / `gemini` / `openai` から選択可能。

---

## 🔗 関連リポジトリ

| リポジトリ | 役割 |
|-----------|------|
| [fortune-core](https://github.com/norinori-jan/fortune-core) | 梅花心易エンジン・registry CDN配信 |
| [fortune-registry](https://github.com/norinori-jan/fortune-registry) | プロンプト・タロットデータ管理 |
| [fenshui_map](https://github.com/norinori-jan/fenshui_map) | 風水マップ（React + Firebase） |
| [security-hub](https://github.com/norinori-jan/security-hub) | セキュリティ統合ダッシュボード |

---

## 📦 技術スタック

| レイヤー | 技術 |
|---------|------|
| API | FastAPI + uvicorn（Python） |
| AI | Anthropic Claude / Google Gemini / OpenAI GPT |
| フロントエンド | Vanilla JS + SVG（依存ゼロ） |
| データ | JSON（registry_a.json） |
| ホスティング | Render（API）/ GitHub Pages（UI） |
| CI/CD | GitHub Actions |
