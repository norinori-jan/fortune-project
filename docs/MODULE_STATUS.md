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

## 2026-10-26 追記：サーバー API の状態
`server/app.py` が `server/fortune_*.py` の router を全部つなぐ形になった（約 145 本の入口）。
試験呼び出しの結果：正常 112 ／ 入力が足りず 422 18 ／ **内部エラー 6**。
内部エラー 6（`/fortune/bundle` `/fortune/compare` `/fortune/pipeline` `/fortune/theme-cycle` `/fortune/period-view/{user}` `/fortune/content/{user}/periods`）は、
「総合占い（complete）」の返す形が、呼び出し側の想定（`.unified` `.tarot` `.meihua` を持つ形）とずれている、
あるいは `PeriodFortuneService.get` など呼び先のメソッドが無いという、設計の世代違い。次の作業で揃える。
本節の修理：`FortuneHubService` に `today()` と `user_key` 引数を追加、`FortuneShare.to_dict` に `id`、
`runtime_contract` の `name`/`key` 両対応、`platform` が `FortuneRunner` を公開。

## 2026-10-26 追記2：総合占い（complete）の形を案Aに揃えた
`CompleteFortuneService.divine(question, theme)` は `CompleteFortuneResult` を返す。
`.unified`（message/advice/keywords/title）、`.tarot`、`.meihua`（title/trigram_name/keywords）を別々に持ち、
総合の項目（question/theme/overall/message/items/keywords/advice）も同名で読める。
これで bundle / compare / pipeline / theme-cycle / period-view / content periods の内部エラー 6 本が解消。
試験呼び出しでの内部エラーは 0 本。

## Render（iPhone 用）
- 見る先のブランチを consolidate/hub-revive にすると、https://<サービスURL>/app で画面が開く。
- main は変更しない。戻すときは Render のブランチ設定を main に戻すだけ。

## 2026-10-26 追記3
- `engine.py` の import を `iching/interpreter.py`（ReadingResult と InterpretationEngine の実体）に向けた。読み込みはできるが、`cast_coin()` は CoinCast と HexagramResult の型違いで実行時に失敗する（易の旧版・新版の食い違い。画面は使っていない）。
- `shichu/astronomy.py` は本体が無いまま（1 行の呼び出しのみ）。
- 画面に「共有する」を追加（/fortune/share で共有データを作り、iPhone の共有シート、無ければコピー）。

## 2026-10-27 四柱推命：skyfield を Render に入れるか
結論：**入れない**（今の簡易計算を残す）。
- 簡易計算の節入り時刻は、春分・立春などの実際の時刻に対し ±10 分以内（検証：2020〜2025 の春分と、2023・2025 の立春。日本時間）。
- 本格版（shichu/calendar.py）は skyfield＋scipy＋天体暦ファイル（数十 MB を実行時に取得）が要る。Render 無料枠（512MB）では重く、再起動のたびに取得し直す。また engine.py 側に未定義変数（solar_terms_json_path）があり、そのままでは動かない。
- 代わりに、節入りの前後約15分以内では「暦の確認が必要」と画面に出すようにした（`boundary_warning`）。
- 本格版が要るときは、PC 側（ローカル）で skyfield を入れて使う。
