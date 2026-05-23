# README_WIP

最終更新: 2026-03-10

このファイルは、作業再開時に短時間で状況復元できるように作成した WIP メモです。
「実装済み機能」「現在の設定意図」「次に着手する設計案」をまとめています。

---

## 1. これまでの作業内容サマリ

### 1-1. 初期不具合対応
- `reference.md` の内容を `hexagrams.py` に反映。
- ルート 404 を解消（`frontend/dist` 不在時のフォールバック導線を追加）。
- 占い結果がフロントで表示されるよう修正。

### 1-2. 環境変数・起動整備
- backend / frontend で `.env` 運用に統一。
- `VITE_API_BASE_URL` による API ベース URL の環境変数化。
- README を拡張して起動手順・API仕様・運用方法を追記。

### 1-3. Codespaces 対応
- host から `-5000.app.github.dev` / `-5173.app.github.dev` を扱う構成へ対応。
- backend でフロント dev server URL の自動推定ロジックを追加。

### 1-4. 履歴・分析・出力
- SQLite に占い履歴を保存。
- 履歴検索、フィードバック更新、自己評価スコア更新を実装。
- CSV エクスポート（UTF-8 BOM、Sheets/Excel互換対策）実装。
- 週次/月次トレンド API、カテゴリ別比較 API 実装。
- Google Sheets 連携 API 実装。

### 1-5. スマホ UX とオフライン
- safe-area / 100dvh / キーボード被り対策 / 下部ナビ / 折りたたみ履歴に対応。
- オフライン時の履歴・分析キャッシュ表示を実装。
- フィードバック更新のオフラインキューを実装（オンライン復帰で再送）。
- 新規占いは「自動保存ではなく確認ダイアログ後にキュー保存」へ変更済み。

---

## 2. 実装済み機能ステータス

### 2-1. スマホ対応
状態: **実装済み**

主な内容:
- `visualViewport` を使ったキーボード検知。
- iOSでの入力フォーカス時 `scrollIntoView` による被り軽減。
- モバイル下部ナビ（占い / 履歴 / 分析）。
- 履歴カードの折りたたみ表示。
- `safe-area-inset` 考慮のレイアウト。

### 2-2. ローカル占い（オフライン時の新規占い取り扱い）
状態: **実装済み（確認付き）**

主な内容:
- 新規占い送信失敗時、ユーザーに確認ダイアログを表示。
- 同意時のみ端末キュー（localStorage）に保存。
- オンライン復帰時にキューを自動送信。

補足:
- 「勝手に保存しない」ポリシーに変更済み。

### 2-3. URL 自動推定
状態: **実装済み**

主な内容:
- backend がアクセス元 host を見て、Codespaces 用フロント URL を推定。
- `FRONTEND_DEV_SERVER` 未指定時も、可能な範囲で dev server へ誘導。

---

## 3. 現在のアプリ状態（2026-03-10 時点）

## 3-1. バックエンド
- フレームワーク: Flask
- DB: SQLite
- 主な API:
  - `POST /api/divine`
  - `GET /api/trigrams`
  - `GET /api/health`
  - `GET /api/divinations`
  - `PATCH /api/divinations/:id`
  - `GET /api/divinations/export.csv`
  - `GET /api/divinations/stats/trend`
  - `GET /api/divinations/stats/categories`
  - `POST /api/divinations/export/sheets`

DB 初期化:
- アプリ起動時に `init_db()` 実行。
- 必要カラムの不足があれば `ALTER TABLE` で補完。

## 3-2. フロントエンド
- フレームワーク: React + Vite
- 画面:
  - 占い
  - 履歴一覧
  - 分析
- concernType（相談カテゴリ）とテンプレ質問あり。
- オフライン時:
  - 履歴 / 分析 / カテゴリ統計を localStorage から表示可能。
  - フィードバック更新、新規占い（同意時）をキューして復帰後再送。

## 3-3. テスト/ビルド
- backend pytest は直近で成功（43 passed）。
- frontend は lint / build とも成功。

---

## 4. 現在の .env 設定意図

対象: `backend/.env`

```dotenv
GOOGLE_API_KEY=REPLACE_WITH_NEW_KEY
PORT=5000
FLASK_DEBUG=1
FRONTEND_DEV_SERVER=https://glorious-space-pancake-x5rrprxrq9gvfp6v9-5173.app.github.dev
```

意図:
- `GOOGLE_API_KEY`
  - Gemini 呼び出し用キー。
  - 現在はプレースホルダ（露出対策のため実値を削除済み）。
- `PORT=5000`
  - backend API / 配信ポート。
- `FLASK_DEBUG=1`
  - 開発用デバッグ有効。
- `FRONTEND_DEV_SERVER`
  - `frontend/dist` が無い時に転送するフロント開発サーバーURL。
  - Codespaces の 5173 側 URL を明示して 404 を避けるため。

セキュリティ運用:
- `.env` / `**/.env` は `.gitignore` 済み。
- `.env.example` は共有用に追跡維持。
- APIキーは必ずローテーションしたものを再設定すること。

---

## 5. 再開時に着手する設計案（履歴保存用DBの実装）

> 注意: 現時点で SQLite 保存は実装済み。
> ここでは「再開時の本命タスク」を **履歴保存DBの強化・再設計（v2）** として定義。

## 5-1. 目的
- 履歴保存を今後の運用（分析、オフライン同期、再送）に耐える構成へ拡張する。
- スキーマ変更に強い migration 管理を導入する。

## 5-2. 提案アーキテクチャ
1. DB 層を `app.py` 直書きから分離
- 例: `backend/db.py`, `backend/repositories/divinations.py`
- SQL と API ロジックを分離し、テストしやすくする。

2. migration 管理導入
- 方式A: Alembic 導入（推奨）
- 方式B: 現在方式を維持しつつ `schema_version` テーブルで段階管理

3. テーブル再設計（最小拡張）
- `divinations`
  - 既存列維持。
  - `status`（active/deleted）を追加して論理削除対応。
  - `updated_at` を追加。
- `sync_events`（新規）
  - `id`, `event_type`, `payload_json`, `created_at`, `processed_at`, `status`
  - オフライン再送の監査・障害調査用。

4. インデックス整備
- `created_at`, `person_name`, `self_score`, `category`, `evaluated_at` に索引。
- 検索クエリの実行計画を確認して必要最小限に調整。

## 5-3. API 側変更案
- `GET /api/divinations`
  - page/limit 方式のページング追加。
  - 既存フィルタとの互換維持。
- `POST /api/divine`
  - 保存失敗時のリトライ方針を明文化。
- `PATCH /api/divinations/:id`
  - 更新競合（楽観ロック）導入検討。

## 5-4. オフライン連携（DB視点）
- フロントの pending キューは維持。
- サーバ側では重複送信を避けるため、`client_request_id` の採用を検討。
  - 同じ `client_request_id` は冪等に扱う。

## 5-5. 実装ステップ（再開時ToDo）
1. 現行スキーマの ER 図を README_WIP に追記。
2. migration 方針決定（Alembic採用可否）。
3. `updated_at`, `status` 追加 migration 作成。
4. インデックス migration 作成。
5. repository 層へ SQL 抽出。
6. API テスト更新（ページング、競合、冪等）。
7. フロントの一覧取得をページング対応。

## 5-6. 受け入れ条件
- 既存 API の互換を壊さない。
- 既存テスト + 追加テストが全件成功。
- データ移行後も既存履歴が欠落しない。
- オフライン復帰時の再送で重複レコードが発生しない。

---

## 6. 再開時クイックスタート

1. 依存関係確認
```bash
cd /workspaces/fortune/backend && pip install -r requirements.txt
cd /workspaces/fortune/frontend && npm install
```

2. .env の実値反映
- `backend/.env` の `GOOGLE_API_KEY` を新キーへ更新。

3. 起動
```bash
# terminal 1
cd /workspaces/fortune/frontend && npm run dev

# terminal 2
cd /workspaces/fortune/backend && python app.py
```

4. 動作確認
- 占い実行（オンライン）
- オフライン化して新規占い実行（確認ダイアログが出ること）
- オンライン復帰後に自動再送されること

---

## 7. 備考
- セキュリティ上、過去に露出したAPIキーは再利用しないこと。
- 次回の会話ではこのファイルを読み込ませれば、同一前提で即再開可能。