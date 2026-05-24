# fortune-project アーキテクチャ仕様書

## リポジトリ構造

```
fortune-project/
├── core/
│   ├── registry_a.py        ← SSOT生成スクリプト（ここだけ編集）
│   ├── registry_a.json      ← 生成物（コミットして fortune-core に push）
│   └── shared/
│       ├── cosmology.js     ← 八卦・五行・十二支・六十四卦データ型
│       ├── timeAxis.js      ← 干支・九星・梅花心易 時間計算
│       ├── reading.js       ← DivinationReading型・ReadingBridge
│       └── ui-tokens.css    ← 全アプリ共通デザイントークン
│
├── apps/
│   ├── iching/              ← 易・梅花心易アプリ
│   ├── tarot/               ← タロットアプリ
│   ├── lopan/               ← 羅盤・風水アプリ（fengshui-app統合）
│   └── fortune-hub/         ← 複合ハブ（全ツール俯瞰）
│
├── prompts/
│   ├── system/              ← Claude APIシステムプロンプト
│   └── reading-templates/   ← 読み解きテンプレート
│
└── docs/
    ├── ARCHITECTURE.md      ← このファイル
    └── INTEGRATION_SPEC.md
```

## データフロー

```
registry_a.py
    ↓ python3 registry_a.py
registry_a.json  ──push──→  fortune-core (GitHub Pages)
    ↓ fetch
各アプリ (iching / tarot / lopan)
    ↓ ReadingBridge.convert()
DivinationReading
    ↓ ReadingBridge.synthesize()
fortune-hub (五行レーダーチャート)
```

## GitHub配置

| ローカル | GitHub リポジトリ | GitHub Pages |
|---------|-----------------|-------------|
| `core/registry_a.json` + `core/shared/*` | `fortune-core` | **有効** |
| `apps/iching/*` | `fortune-project` | 無効 |
| `apps/lopan/*` | `fortune-project` | 無効 |
| `apps/tarot/*` | `fortune-project` | 無効 |

## 各アプリのアダプター実装パターン

```javascript
// apps/iching/src/adapter.js
import { ReadingBridge, scoreToWuxing } from '../../core/shared/reading.js';
import { getCurrentTimeContext } from '../../core/shared/timeAxis.js';

ReadingBridge.register('iching', (rawResult) => {
  // rawResult = DivinationEngine の出力（rokko_divination.py の結果）
  const yongWuxing = rawResult.yongShenWuxing; // 'wood'|'fire'|...
  return {
    tool: 'iching',
    timestamp: Date.now(),
    wuxing: scoreToWuxing(yongWuxing, rawResult.score),
    timeContext: getCurrentTimeContext(),
    reading: {
      core:   rawResult.verdict,          // '吉'|'大吉'|...
      detail: rawResult.detail,
      action: rawResult.actionAdvice ?? '',
    },
    symbols: [rawResult.hexName, rawResult.yongShenKanji],
    resonance: ReadingBridge.suggestResonance({ wuxing: scoreToWuxing(yongWuxing, rawResult.score) }),
  };
});
```

## 禁止事項

- `core/shared/` の外でハードコードされた色値・フォント定義
- `DivinationReading` を経由しないツール間データ受け渡し
- `registry_a.json` をネットワーク取得のみに依存（必ずオフラインフォールバック）
- 各アプリが独自に八卦・十二支データを定義する
