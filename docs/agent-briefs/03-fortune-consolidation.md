# 依頼 03：占いの統合（5リポジトリ → `fortune-project` に一本化、入り口を1つに）

> これは大きい依頼です。**フェーズごとに別々の PR** にしてください（まとめて1つにしない）。各フェーズの終わりで、人（Nori）が確認してから次へ進みます。

## 目的
- たくさんに分かれた占いのリポジトリを、`fortune-project`（= hub）に一本化し、**入り口を1つ**にする。
- 元データ（64卦・タロット・八卦・羅盤など）は `core/registry_a.json` の1か所（SSOT）にする。
- いまの動作（API・画面・テスト）を**壊さない**。

## いまの状況（下準備で調べた事実。読み取りだけ・中身は未検査）
| リポジトリ | ファイル数 | 最新 | hub（`fortune-project`）との関係 |
|---|---|---|---|
| fortune-project | 434 | 2026-08-09 | hub 本体。`apps/fortune-hub/index.html`（入り口の候補）、`server/`（FastAPI・Render）、`core/`（SSOT）、`fortune/`、`ninso/`。他4つのコピーを内側に含む |
| fortune-registry | 38 | 2026-05-23 | hub の `fortune-registry/` に、38中**35が同一**。違い：`prompts/meihua.json`、`tarot/major.json`。hub に無い：`prompts/meihua.json.broken`（壊れた版。不要の可能性が高い） |
| fortune-core | 33 | 2026-05-22 | hub の `fortune-core/` と**構成が違う**（単体は `src/fortune_core`、hub 側は `fortune-core/fortune_core`）。**単体にだけある15ファイル**：`demos/*`、`tarot_cards.json`、`divination_entry.py`、`report_generator.py`、`src/meihua/*.js`、`bian_gua.json`、`hu_gua.json` ほか。内容が違うもの：`api.py`、`hexagrams.py`、`tarot_engine.py` ほか |
| fengshui-app | 72 | 2026-05-10 | hub の `apps/lopan/` に、**60が同一**。違い：`frontend/src/App.jsx`、`api.js`、`lopanDatabase.js`、`vite.config.js`。**開発用の鍵ファイル**（依頼01で除去） |
| lopanproject | 75 | **2026-08-16（hub より新しい）** | 構成がまったく別（`data/layers`、`core/lopan/integrity`、`api/lopan/ar_api.py`、`js/`、`python/`）。hub の `apps/lopan/` は、**古い fengshui-app のコピー**で、lopanproject が**新しい版**に見える |

重要：`lopanproject` が最新です。`apps/lopan/` を、そのまま正とせず、**羅盤（Lopan）は lopanproject を基準**にして、fengshui-app のうち有用な部分（24山の判定、iPhone 向けカメラ/方位センサー UI）を取り込む形が自然です（要確認。決めるのは人）。

## フェーズ
### P0：棚卸し（読み取りのみ・PR は文書だけ）
- `docs/CONSOLIDATION_INVENTORY.md` を作る。内容：5リポジトリ × 全ファイルの対応表（同一／内容違い／片方のみ）、ハッシュ、最終更新、各モジュール（易・タロット・四柱・羅盤）の正の置き場所の**提案**と理由。
- テストの現状：どのテスト（`fortune-core/tests`、`server/tests`、六爻の22テストなど）が、どのコマンドで、いま通るか／通らないかを、**実行して**表にする。
- 完了の条件：表が完成し、「判断が要る点」が一覧になっている。

### P1：判断の確定（人）
- Nori が、P0 の「判断が要る点」に答える。ここで止まる。

### P2：統合（モジュールごとに、別 PR）
- 順番：registry（SSOT）→ fortune-core → 四柱 → 易 → 羅盤。
- 移すたびに：テストを実行し、**移す前と同じ結果**であることを PR に書く。
- 元のリポジトリは**消さない**。README の先頭に「◯◯は fortune-project/◯◯ に移りました」と書く PR だけを、最後に出す（アーカイブは人が行う）。
- `.broken` ファイル、重複するコピー（`fenshui_map/fortune-core` など）は、**消す前に一覧**を出して、人の確認を待つ。

### P3：入り口を1つにする（`apps/fortune-hub/index.html`）
- 開くと、**4枚のカード**（易／タロット／風水・羅盤／四柱推命）と、「最近使った」が出る。1タップで各画面へ。
- PWA にする（manifest・sw.js・アイコン。iPhone のホーム画面に置ける）。API の接続先（Render）は、設定画面で入れる形にし、**キー類はリポジトリにもフロントにも入れない**（サーバー側の環境変数だけ）。
- 画面は、スマホ最優先。ボタンは押しやすく、迷わない文言（「占う」「結果を見る」など）。
- 完了の条件：iPhone Safari の幅で、4つの入口がスクロールなしで見える。各カードから、動いている画面に行ける。

### P4：文書
- `README.md` を「入り口の地図」にする（どこに何があるか、1画面で）。`docs/ARCHITECTURE.md` を、統合後の姿に更新。

## 守ること（この依頼に固有）
- 鑑定の文書・画像（`fenshui_map/assets/lopan_raw/`、`fortune-registry/sources/textbook/`、`prompts/`、`fortune/backend/reference.md` など）は、**移動も削除もしない**。場所と枚数だけを P0 に書く。
- 公開のまま運用します（有料化のため）。ただし、**他人の文章・写真**（教科書のページ写真に見えるもの）は、著作権の確認が要るファイルとして、PR に一覧で報告してください（消さない）。
- 履歴の書き換え・強制 push はしない。

## 完了の定義（全体）
入り口が1つ。元データが1か所。統合前に通っていたテストは、全部通る。READMEだけで、新しい人（未来の自分）が迷わない。

---
## 追記（2026-10-24）
- 下準備の棚卸しは古い clone に基づく。fengshui-app には、その後 `registry_a.json`、`src/web/FortuneWeb/engines/{YiEngine,ExportEngine}.ts`、`static/registry-loader.js` などが追加されている。フェーズ0の棚卸しは、必ず各リポジトリの最新の main から作り直すこと。表の数字は信用しない。
- fengshui-app の鍵ファイル除去は push 済み（d6a0509）。
- 羅盤の置き場所は、cad-core の三次元地勢（05）と関係する。羅盤の方位（24山）を地形に重ねる使い方があるので、置き場所の提案は、05 と同じ入口・同じデータ形式で使えるかを必ず検討すること。
