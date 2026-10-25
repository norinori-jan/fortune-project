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

## 同じ日に追加したもの（新規）
| 場所 | 中身 |
|---|---|
| `fortune_core/entry_router.py` | 相談内容 → 4つの占い（易・タロット・風水/羅盤・四柱）のどれを勧めるか（キーワードの規則） |
| `fortune_core/shichu_simple.py` | 四柱（年・月・日・時）の簡易計算。日柱はユリウス日、年・月は太陽黄経で節入りを判定。既存の `shichu/engine`（壊れている）とは別 |
| `server/fortune_entry_api.py` | `POST /fortune/entry`、`POST /fortune/tarot/celtic`、`POST /fortune/shichu/pillars` |
| `apps/fortune-hub/entry.html` | **占いの入り口の画面**（質問 → おすすめ → 占う → 履歴）。スマホ幅・単一ファイル |
| `run_entry.ps1` | この PC で、サーバーと入り口を起動して開く |

四柱の簡易計算は、2000-01-01 12:00（己卯・丙子・戊午）、2024-01-01（甲子日）、立春（2024-02-04 17:27 JST）の前後での年・月の切り替わりで確認済み。
