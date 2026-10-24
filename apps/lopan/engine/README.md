# 羅盤エンジン（lopanproject から取り込み）

- `integrity/`：角度の整合性・層の照合（Layer 10〜27）
- `api/ar_api.py`：AR 用の測定→照合の核
- `lopan_service.py`：**Raw を読み込み、角度から各層の記載を引く入口**（`measure(角度)`／`verify(角度)`）。読み取り専用
- `python/`、`js/`：補助（空ファイルは取り込んでいない）
- `tests/`：`pytest apps/lopan/engine/tests`（4件）

出どころ：norinori-jan/lopanproject（2026-08-16 時点）。元のリポジトリは消さない。
方針：Raw は変更しない。意味付け・吉凶判定は、現段階では行わない。

## 現状（2026-10-25・実際に動かして確認）
| 層 | 状態 |
|---|---|
| 10〜13、24、26 | 角度 330° で記載が1件ずつ引ける（OK） |
| 14 | 330° では引けるが、0° などでは未一致（区間の持ち方が別） |
| 15〜23 | **未一致が多い**（層ごとに角度の書き方が違う。照合側（Layer Adapter）が未対応） |
| 25 | 区間が重なって複数件ヒット（OVERLAP） |
| 27 | **未登録**（`raw_layer27` が関数で組み立てる形式のため、まだ読めていない） |
| 22 | 記録が1件しか読めていない（Raw の書式を確認が必要） |

## 取り込みで直した点（Raw 以外）
- `integrity/angle_integrity_scanner.py`：`StandardAngleLayerLayerAdapter` → `StandardAngleLayerAdapter`（クラス名の綴り間違い。直さないと照合が動かない）
- `lopan_service.py` が、標準の層の `degree_start/degree_end` を `angle_start/angle_end` の別名つきコピーにして渡す（Raw は変えない）

## Raw ファイルの注意（元のまま）
- そのままでは Python として読めない（先頭の説明文の引用符が欠け、末尾に壊れた関数が混ざる）。`lopan_service.py` は、`raw_layerNN = [ ... ]` の部分だけを取り出して使う。
- `layer17` の中に層18、`layer22` の中に層21、`layer23` の中に層24 のデータが混ざっている。
