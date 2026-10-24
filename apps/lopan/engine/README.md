# 羅盤エンジン（lopanproject から取り込み）

- `integrity/`：角度の整合性・層の照合（Layer 10〜27）
- `api/ar_api.py`：AR 用の測定→照合の API の核
- `python/`、`js/`：層データの読み込み・生成・描画の補助（空ファイルは取り込んでいない）
- `tests/`：取り込んだものが読み込めて基本の動きをするかの確認（`pytest apps/lopan/engine/tests`）

出どころ：norinori-jan/lopanproject（2026-08-16 時点）。元のリポジトリは消さない。
方針：Raw Database は変更しない。意味付け・吉凶判定は、現段階では行わない。
