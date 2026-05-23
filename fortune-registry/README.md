# fortune-registry

占術データの正典リポジトリ。
JS（fortune-core）・Python（fortune）両方がここを参照する。

## 構造

| パス | 内容 |
|------|------|
| prompts/ | 占術ごとのプロンプト定義（高亨四分類・断占フレーム） |
| tarot/ | タロット基本データ・card_notes（Nori吹き込み）・sessions |
| meihua/ | 梅花心易データ（六十四卦・五行） |
| shichu/ | 四柱推命データ（準備中） |
| registry.json | 全占術のエントリーポイント |

## 参照方法

GitHub Pages経由でfetchする。
IndexedDBにキャッシュしてオフライン対応。

## Base URL

https://norinori-jan.github.io/fortune-registry/

## 更新ルール

- データ修正は必ずこのリポジトリだけで行う
- fortune-core（JS）・fortune（Python）はここをfetchするだけ
- card_notesはNoriの吹き込みセッション後に随時更新
