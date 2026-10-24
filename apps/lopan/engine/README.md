# 羅盤エンジン（lopanproject から取り込み）

- `integrity/`：角度の整合性・層の照合（Layer 10〜27）
- `api/ar_api.py`：AR 用の測定→照合の核
- `lopan_service.py`：**Raw を読み込み、角度から各層の記載を引く入口**（`measure(角度)`／`verify(角度)`）。読み取り専用
- `python/`、`js/`：補助（空ファイルは取り込んでいない）
- `tools/`：`make_dict_pack.py`（辞書パックを作る）、`layer_report.py`（層ごとの状態表を作る）
- `tests/`：`pytest apps/lopan/engine/tests`（6件。Raw が変わっていないことの確認を含む）

出どころ：norinori-jan/lopanproject（2026-08-16 時点）。元のリポジトリは消さない。
方針：Raw は変更しない。意味付け・吉凶判定は、現段階では行わない。

## 現状（2026-10-25・実際に動かして確認。層01〜10 は作り直し中）
`measure(角度)` の status：OK／OVERLAP／NO_MATCH／**PARTIAL_DATA**（角度が一部の区分にしか入っていない）／**NO_ANGLE_DATA**（角度が1つも入っていない）／NOT_REGISTERED。
- **引ける層：** 10〜13、23（隙間あり）、24、25、26、27
- **一部だけ：** 14、19、20、21（Raw に、最初の区分しか角度が入っていない）
- **角度なし：** 15〜18、22（Raw に角度が1つも無い）
- 引けない理由は、**エンジンの不具合ではなく、Raw にまだ角度が無いこと**。詳しくは `apps/lopan/docs/LAYER_DATA_STATUS.md`（自動生成：`tools/layer_report.py`）。
- 照合から外した記録：層25の48番（角度が逆向きに入力されている。要確認）

## 取り込みで直した点（Raw 以外）
- 層27：Raw は記号の並びだけを持ち、角度は規則（329.5°起点・1°刻み）で付ける。元ファイルは関数の字下げが失われていたので、同じ規則を `lopan_service.py` で再現した（記号は原文のまま）。
- `integrity/angle_integrity_scanner.py`：`StandardAngleLayerLayerAdapter` → `StandardAngleLayerAdapter`（クラス名の綴り間違い。直さないと照合が動かない）
- `lopan_service.py` が、標準の層の `degree_start/degree_end` を `angle_start/angle_end` の別名つきコピーにして渡す（Raw は変えない）

## Raw ファイルの注意（元のまま）
- そのままでは Python として読めない（先頭の説明文の引用符が欠け、末尾に壊れた関数が混ざる）。`lopan_service.py` は、`raw_layerNN = [ ... ]` の部分だけを取り出して使う。
- `layer17` の中に層18、`layer22` の中に層21、`layer23` の中に層24 のデータが混ざっている。
