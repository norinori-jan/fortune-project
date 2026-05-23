# frontend

## 開発

```bash
npm install
npm run dev
```

開発サーバーは通常 http://127.0.0.1:5173 で起動します。

## ビルド

```bash
npm run build
```

生成物は frontend/dist に出力されます。

## 環境変数

frontend/.env.example を frontend/.env にコピーして使います。

- VITE_API_BASE_URL
	- 既定: 空文字
	- 空文字のときは相対パス /api/divine にアクセスします（Vite proxy 前提）
	- 静的配信や別ドメイン環境では、例として http://localhost:5000 を設定してください

## オフライン利用

- 取得済みの履歴・分析データは端末の localStorage に自動保存されます。
- ネットワーク断時は保存済みキャッシュを表示します。
- 履歴のフィードバック更新はオフライン時にローカルキューへ積み、オンライン復帰時に再同期します。
