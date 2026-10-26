# fortune_core の読み込めないモジュール（2026-10-26 更新）
全 416 ファイル中、読み込めないのは 2 本（skyfield を入れた場合）。最初は 51 本だった。

## 原因と直し方（「なくなった」のではなかった）
1. ファイル名の先頭 1 文字が欠けていた（`ortune_registry.py`→`fortune_registry.py`、`ive_elements.py`→`five_elements.py` など）。名前を直した。
2. 別ファイルの末尾に「パス行＋中身」として貼られていた（`models/favorite.py` など 18 本）。元の場所に取り出して復元した。
3. `core/services/` に置かれていた `complete_fortune.py` / `unified_fortune.py` と `core/models/unified_fortune.py` を fortune_core 側へ複製した。
4. 貼り付けメモ行・`from __future__` の位置を修正（該当行は `# [貼り付けメモ]` でコメント化。消していない）。
5. 本当に欠けていたのは `platform/fortune_protocol.py` と `models/fortune_share.py` の 2 本だけ。使われ方から最小の形で再作成した（推測を含む）。

## まだ直っていない 2 本
- `shichu/astronomy.py`：中身が `calc_solar_terms()` の 1 行だけ（本体が無い）。
- `engine.py`：`iching.interpretation_modules` から `InterpretationEngine` を読むが、実体は `iching/interpreter.py` と `iching/interpretation.py` に 2 つある。どちらが正か未確認。

## 注意
- 本格四柱（`shichu/calendar.py` ほか）は `pip install skyfield` が必要。
- 画面の履歴・お気に入りは端末保存のまま。
