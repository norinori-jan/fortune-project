# fengshui-app

風水方位判定（24山）と五行強度推定を提供する Flask API、iPhone向けカメラ/方位センサーUI の土台です。

## 1. Backend 起動

```bash
cd /workspaces/fengshui-app
python3 -m pip install -r requirements.txt
python3 app.py
```

- API: `http://localhost:5000`
- エンドポイント:
	- `POST /api/fortune/direction` (`degree` を送信)
	- `POST /api/fortune/strength` (`zodiac_list` を送信)

## 2. Frontend 起動

```bash
cd /workspaces/fengshui-app/frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

Codespaces では `*-5173.app.github.dev` にアクセスすると、フロントが自動で `*-5000.app.github.dev` を API として参照します。

## 3. iPhone での利用手順

1. フロント画面を開く
2. 「センサー許可」を押す
3. カメラ中央オーバーレイで現在の二十四山を確認
4. 下部パネルで五行計算（例: `寅,午,戌`）
5. 「鑑定ボタン」でカメラ映像 + 方位/五行の合成画像を保存