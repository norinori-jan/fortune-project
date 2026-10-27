# 依頼 01：開発用の鍵ファイルの除去（fengshui-app）

目的：秘密鍵のファイルが公開リポジトリに入っているので、外して、今後入らないようにする。
対象：`norinori-jan/fengshui-app` の `frontend/localhost+2-key.pem` と `frontend/localhost+2.pem`。
やること：
1. 上の2ファイルを、リポジトリから外す（`git rm`）。
2. `.gitignore` に `*.pem` `*.key` `.env` `.env.*` を足す。
3. README に「ローカルで https が要るときは `mkcert localhost` で作り直す（鍵は入れない）」と1行足す。
4. 他の4リポジトリ（fortune-project / fortune-core / fortune-registry / lopanproject）にも、同じ種類のファイルがないか確認し、あれば同じ扱い（無いはず）。
完了の条件：`git ls-files | grep -E "\.(pem|key)$"` が何も出さない。PR の説明に、確認コマンドと結果。
しないこと：履歴の書き換え（開発用の localhost の鍵なので、失効させる必要は小さい。必要なら人が決める）。
手元でやる場合の手順：`fengshui-app/remove-pem.ps1`（同梱）。
