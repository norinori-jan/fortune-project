# ninso（人相鑑定）

- index.html / app.js : 写真から三停などを測る画面
- data/public/        : 型の名前と判定条件（公開してよい）
- data/private/       : 巻ごとの書き起こし全文（dai01.json, dai02.json …）。.gitignore で公開しない

## 巻の追加手順
1. PDF を Claude に渡して書き起こしてもらう（JSON を受け取る）
2. Downloads に dai02.json のように置いて、ninso-setup.ps1 を実行すると data/private/ にコピーされる
3. 節の題から型・部位のキーを付ける（Claude に依頼）

## 使い方（サーバー）
- GET  /fortune/ninso/volumes … 読み込めている巻
- POST /fortune/ninso/lookup  … {"key":"yu"} か {"query":"運"} で、巻とページ付きの該当節を返す
