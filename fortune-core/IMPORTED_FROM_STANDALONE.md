# 単体の fortune-core から取り込んだもの（2026-10-25・追加のみ）

出どころ：norinori-jan/fortune-core（2026-05-22 時点）。元のリポジトリは消さない。

| 取り込み先 | 中身 |
|---|---|
| `fortune_core/divination_entry.py` | **占いの入口**：相談内容を分類（恋愛・仕事・金運など）し、おすすめの占術と案内文を返す（`DivineEntryEngine`） |
| `fortune_core/tarot_engine.py` ＋ `fortune_core/data/tarot_cards.json` | タロット 78枚・ケルト十字（10枚）（`TarotEngine`）。同じ seed なら同じ結果 |
| `fortune_core/report_generator.py` | 鑑定レポート生成 |
| `src/meihua/` | 梅花心易の JavaScript エンジン一式（README の構成どおりの置き場所） |
| `demos/` | 動作デモ（`PYTHONPATH=fortune-core` で実行） |

つないだもの：`server/fortune_entry_api.py`（`POST /fortune/entry`、`POST /fortune/tarot/celtic`）を `server/app.py` に追加。
**つないでいないもの：** 梅花心易の JS（まだ画面・API から呼んでいない）、報告書生成、単体の `api.py`（hub 側のほうが新しいため取り込まない）。
既存のファイルは書き換えていない（`server/app.py` の末尾に、読み込めなくても動く追記が1か所あるのみ）。
