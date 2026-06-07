# 🔮 タロット鑑定エンジン強化ロードマップ

## 概要

iPhoneで鑑定内容を録音→文字起こし→データ蓄積→AIエンジン強化のサイクルを構築する。

---

## Phase 1: 録音・文字起こし（iPhone）

### 方法A: iPhone標準機能を使う（今すぐできる）

1. **ボイスメモ**アプリで鑑定中の発言を録音
2. 録音後、共有ボタン→「テキストに変換」（iOS17以降で利用可能）
3. テキストをメモアプリにコピー保存

### 方法B: アプリ内録音ボタンを追加（実装予定）

```
index.html に録音ボタンを追加
↓
Web Speech API で音声→テキスト変換
↓
鑑定結果と紐付けてサーバーに送信
↓
registry_a.json に保存
```

### 方法C: Whisper API を使う（高精度）

```python
# server/app.py に追加予定
import openai

@app.route("/api/transcribe", methods=["POST"])
def transcribe():
    audio_file = request.files["audio"]
    transcript = openai.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="ja"
    )
    return jsonify({"text": transcript.text})
```

---

## Phase 2: データ蓄積

### registry_a.json の拡張スキーマ

```json
{
  "tarot": [
    {
      "session_id": "2026-06-07-001",
      "drawn_at": "2026-06-07T12:00:00",
      "spread": "celtic",
      "question": "転職すべきか",
      "cards": [...],
      "ai_reading": {
        "gemini": "鑑定文...",
        "claude": "鑑定文..."
      },
      "voice_memo": {
        "transcript": "実際の鑑定発言テキスト",
        "recorded_at": "2026-06-07T12:05:00",
        "duration_sec": 180
      },
      "feedback": {
        "accuracy": 4,
        "notes": "潜在意識のカードが特に当たっていた"
      }
    }
  ]
}
```

---

## Phase 3: エンジン強化

### 3-1. system_prompt の改善

録音データから「当たった表現」「響いた言葉」を抽出し、
`server/app.py` の `SYSTEM_PROMPT` を継続的に更新する。

```
fortune-registry/prompts/tarot.json
↑ ここにnoriオリジナルの鑑定スタイルを蓄積
```

### 3-2. カード解釈の個人化

```json
// fortune-registry/tarot/card_notes/ 配下に蓄積
{
  "M00": {
    "nori_interpretation": "愚者は始まりではなく、手放しの勇気",
    "cases": [
      {"question": "転職", "reading": "...", "outcome": "実際に転職して良かった"}
    ]
  }
}
```

### 3-3. Google Sheets との連携

```
iPhone 録音
→ 文字起こし
→ GAS (Google Apps Script) でシートに追記
→ 蓄積データをGeminiに学習させる
```

---

## Phase 4: 実装優先順位

| 優先度 | 機能 | 難易度 | 効果 |
|--------|------|--------|------|
| ★★★ | ボイスメモ→手動テキスト入力欄をUIに追加 | 低 | 高 |
| ★★★ | フィードバック（★評価）ボタンをUIに追加 | 低 | 高 |
| ★★☆ | Web Speech API で自動文字起こし | 中 | 高 |
| ★★☆ | Google Sheetsへの自動同期 | 中 | 中 |
| ★☆☆ | Whisper API 音声→テキスト | 高 | 高 |

---

## 次のアクション

```powershell
# 1. まず手動メモ入力欄をUIに追加
# index.html に鑑定後メモ欄を追加

# 2. GAS URLを設定してSheetsに同期
# server/.env に GAS_URL を追加

# 3. 蓄積データを元にsystem_promptを更新
# fortune-registry/prompts/tarot.json を編集
```

---

*作成: 2026-06-07 | fortune-project v1.0*
