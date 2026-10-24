# 占い5リポジトリの棚卸し（フェーズ0）

調べた日：2026-10-25　／　基準：`fortune-project` の `rebuild/fortune-hub` ブランチ（最新の作業）
方法：5つのリポジトリを GitHub から取り直し、ファイルの中身の同一性（git のハッシュ）で突き合わせた。**コードは変更していない。** 読み取りと、テストの実行だけ。
注意：「同じ」は中身が一字も違わないこと。「違う」は、同じ名前のファイルがあって中身が違うこと（新旧の判断はまだしていない）。

---

## 1. 全体の地図（先に結論）

| リポジトリ | ファイル数 | 最終更新 | 役割 | hub との関係 |
|---|---|---|---|---|
| **fortune-project**（hub） | main 434 ／ rebuild 843 | main 2026-08-09 | API（FastAPI・Render）、入口 UI、SSOT（`core/registry_a.json`） | これが本体 |
| fortune-registry | 38 | 2026-05-23 | プロンプト・タロット・四柱・教科書の写真 | 38中 **34 が hub の `fortune-registry/` と同一**、違い3、hub にないもの1 |
| fortune-core | 33 | 2026-05-22 | 占術ライブラリ（Python／梅花心易 JS） | **構造が別**（単体は `src/fortune_core`、hub は `fortune-core/fortune_core`）。同一 8／違い 10／hub にない **15** |
| fengshui-app | 70 | 2026-10-24 | 羅盤アプリ（Flask API＋React） | 70中 **64 が hub の `apps/lopan/` と同一**、違い6、hub にないもの 0 |
| lopanproject | 75 | 2026-08-16 | 羅盤 AR の土台（層データ 10〜27、検証エンジン） | **中身の半分近くが空ファイル**（§5）。hub にない 32 |

**ひとことで：** `fengshui-app` と `fortune-registry` は、ほぼ丸ごと hub の中に入っている。残る本当の別物は、`fortune-core`（単体にだけある15ファイル）と `lopanproject`（層データ 10〜27 と検証エンジン）。

---

## 2. hub の二つのブランチ

`main`（434 ファイル）と `rebuild/fortune-hub`（843 ファイル）の差：追加 409、変更 3、削除 0。

| 追加の中身 | 数 |
|---|---|
| `fortune-core/fortune_core/` （services 228、models 95 ほか） | 330 |
| `server/` （画面まわり・ハブ API のモジュール） | 69 |
| `docs/agent-briefs/` | 4 |
| `core/models`、`core/services` | 各 3 |

変更された3ファイル：`fortune-core/fortune_core/engine.py`、`fortune-core/fortune_core/iching/iching_registry.py`、`fortune-registry/README.md`。
**`main` から消えたものはない。** つまり `rebuild/fortune-hub` は `main` の上に積んだ作業で、統合の基準にしてよい（人の確認は要る）。

---

## 3. 5つの突き合わせ（詳細）

### 3.1 fortune-registry → hub の `fortune-registry/`
- 同一 34、違い 3（`README.md`、`prompts/meihua.json`、`tarot/major.json`）、hub にない 1（`prompts/meihua.json.broken`）。
- `prompts/meihua.json` の違いは大きい（差分 1383 行）。`tarot/major.json` も 254 行。**どちらが新しいか未確認。**
- `*.broken` は名前から壊れた退避ファイルと思われる（中身は未確認）。

### 3.2 fortune-core（単体）→ hub
- 単体の構造：`src/fortune_core/`（Python）、`src/meihua/`（JS）、`demos/`、`index.html`。
- hub の構造：`fortune-core/fortune_core/`（services 228、models 95、iching 21、shichu 16 …）。**単体より大幅に大きく育っている。**
- **hub にない15ファイル**（単体にだけある）：
  `demos/demo_complete_flow.py`、`demos/demo_tarot.py`、`src/fortune_core/data/tarot_cards.json`、`divination_entry.py`、`report_generator.py`、`src/meihua/{calcJudgeKey,meihuaEngine,templateEngine,utils}.js`、`src/meihua/data/{bian_gua,hu_gua,time_support}.json`、`src/meihua/{registries,strategies}/*.js`。
  → 特に **梅花心易の JS エンジン一式**は hub の `fortune-core` 側に見当たらない。
- 違う10：`api.py`（単体 367 行／hub 126 行、差分 472 行）ほか。

### 3.3 fengshui-app → hub の `apps/lopan/`
- 同一 64。違い 6：`frontend/src/App.jsx`（差分 759 行。単体 332 行／hub 839 行）、`api.js`、`lopanDatabase.js`、`vite.config.js`、`.gitignore`、`frontend/dist/index.html`。
- 鍵ファイル（pem）は 2026-10-24 に除去・push 済み（d6a0509）。hub には pem はない。
- `frontend/dist/index.html` は hub 側では `apps/fortune-hub/index.html` と同名で出会うが、別物（ビルド生成物）。

### 3.4 lopanproject → hub
- 同一とされた 40 件は、**すべて中身が空（0バイト）のファイル同士の一致**。実質の一致ではない（§5）。
- 本当に違う・hub にない：
  - `data/lopan/raw/` の層 10〜27（17ファイル、計 約 212KB。**`lyaer11` `lyaer12` `lyaer15` はファイル名の綴り間違い**と思われる）
  - `core/lopan/integrity/`（検証エンジン4本）、`api/lopan/ar_api.py`
  - `python/`（Geometry、LopanLoader、LopanModel、LopanRenderer、generate_*、utils）、`js/`（LopanLoader、LopanMath、main）
- 違い 3：`README.md`、`docs/lopan/ARCHITECTURE.md`、`python/main.py`。

---

## 4. hub の内側の重複（同じものが複数ある）

| 場所 | 内容 | 状態 |
|---|---|---|
| `fenshui_map/fortune-core/` | fortune-core の古い複製（hexagrams.py ほか、テスト含む） | `fortune-core/` と二重 |
| `fortune/` | 旧 Flask 版（backend／frontend、`reference.md`） | 新 FastAPI（`server/`）と併存 |
| `apps/lopan/` | fengshui-app の複製（64同一） | 単体と二重 |
| `fortune-registry/`、`core/registry_a.json`、`apps/lopan/docs/registry_a.json`、`core/shichu/registry_a.json` | 「registry_a.json」が **3種類**（サイズ 113KB／17KB／26KB、中身が別物） | SSOT と称するものが複数 |
| `fenshui_map/app/` | 空の `__init__.py` が多い | 骨組みだけ |

**SSOT の正：** README は `core/registry_a.json`（113KB）を SSOT と書いている。`apps/lopan/docs` の 17KB と `core/shichu` の 26KB は、別の用途の同名ファイルか、古い版かの判断が必要（§8）。

---

## 5. 空ファイル（0バイト）の一覧

- **lopanproject：40ファイル**。内訳：`data/layers/layer01〜26.json` の26本、`data/master/lopan_master.json`、`data/master/lopan_104_master.csv`、`data/corrections/corrections.json`、`js/LopanCorrectionEngine.js`、`js/LopanRenderer.js`、`python/{generate_corrections,registry,export_csv}.py`、`docs/{CorrectionSpecification,LayerSpecification,README}.md`、`svg/lopan.svg`、`requirements.txt`、`.gitignore`。
  → **GitHub 上では、中身のない「枠」のまま。** 手元に中身があるなら、まだ push されていない可能性が高い。
- hub：19ファイル（`__init__.py`、`.gitkeep` が主。`fortune-core/fortune_core/services/complete_fortune.py`、`fortune_tags.py`、`fortune-registry/shichu/README.md` は**空の実体ファイル**）。
- fortune-registry：2（`.gitkeep` と `__init__.py`）。

---

## 6. テストの現状（実行した結果）

| テスト | 結果 |
|---|---|
| hub `fortune-core/tests`（15件＋7サブテスト） | **全通過** |
| hub `server/tests`（6件） | **全通過** |
| hub `fortune/backend/tests` | **動かない**（`flask_cors` 未導入。旧 Flask 版。環境の問題で中身の可否は未確認） |
| hub `fenshui_map/fortune-core/tests`、`apps/lopan` の JS テスト、六爻22テスト | **未実行**（入口が分かれていて、今回は届かなかった） |
| lopanproject、fengshui-app、fortune-registry、fortune-core（単体） | **未実行** |

---

## 7. 注意が必要なファイル（消す・動かす前に確認）

- **鑑定の秘密文書：** 見つかった候補は `fortune/backend/reference.md` のみ（中身は読んでいない）。Nori さんの話では「読まれても構わない」とのこと。**移動・削除・公開の変更はしない。**
- **画像（他人の著作物の可能性あり。消さない、確認だけ）：**
  - `fortune-registry/sources/textbook/` の写真 4枚（教科書のページに見えるか要確認）
  - `fenshui_map/assets/lopan_raw/` 29枚、`fenshui_map/assets/lopan/` 25枚（羅盤の写真と思われる）
  - `fortune-registry/tarot/` 2枚
- **鍵・秘密：** `.env.example` が3つ（`fortune/backend/`、`fortune/frontend/`、`server/`。見本のみと見られる）。`fenshui_map/scripts/set_gcp_secrets.sh` は、名前に secrets を含むスクリプト（値が入っているかは未確認）。pem は無し。
- **未追跡ファイル（Nori さんの手元）：** `server/fortune_screens.py` などは 2026-10-24 に `rebuild/fortune-hub` へ push 済み。

---

## 8. 判断が要る点（Nori さんが決める）

1. **統合の土台：** `rebuild/fortune-hub` を基準にしてよいか（`main` の上に積んだだけで、`main` から消えたものはない）。
2. **羅盤の置き場所：** `apps/lopan/`（fengshui-app の複製）を正とするか、`lopanproject`（検証エンジンと層 10〜27）を正にするか、両方を一つに合わせるか。
   - 層データ 10〜27 と検証エンジンは lopanproject にしかない。fengshui-app のアプリ画面は hub にある。
   - **cad-core の三次元地勢（05）と同じ入口・同じデータ形式で使えるか**も合わせて考える。
3. **lopanproject の空ファイル40本：** 手元（PC）に中身があるか。あるなら、先にそれを push しないと、統合の元データが欠ける。
4. **梅花心易の JS エンジン**（単体 fortune-core の `src/meihua/*.js` 一式）を、hub に取り込むか。hub 側の梅花（`fortune-core/fortune_core/meihua/`）の中身と重なるか。
5. **registry_a.json が3種類**あるが、どれを SSOT にするか（`core/registry_a.json` 113KB を正とする案）。
6. **fortune-registry の違い2本**（`prompts/meihua.json`、`tarot/major.json`）：どちらが新しいか。
7. **旧 Flask 版 `fortune/`** と **`fenshui_map/`** を、残す／別に退避するか（消すのは人。統合 PR には含めない）。
8. **画像（§7）** の扱い：公開のままでよいか。教科書の写真は、権利の確認をする。
9. 元の4リポジトリを、最後に「移りました」という README だけにして、アーカイブするか（アーカイブは人が行う）。

---

## 9. 次のフェーズの案（P2 の順序）

1. SSOT（registry）→ 2. fortune-core（単体にだけある15ファイルの取り込み方針）→ 3. 四柱 → 4. 易 → 5. 羅盤（判断2・3が済んでから）。
各ステップで、移す前と同じテスト結果になることを確認する。**消すのは、一覧を人が見てから。**
