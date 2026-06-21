## 📍 Registry A Configuration & Deployment Guide

### ✅ 配置状況（fengshui-app）

```
c:\Users\norin\fengshui-app/
├── registry_a.py           (19.4 KB) — 生成スクリプト
├── registry_a.json         (17.0 KB) — 統合レジストリ データ
├── docs/
│   └── registry_a.json     (17.0 KB) — GitHub Pages 公開用
└── static/
    └── registry-loader.js  (7.5 KB)  — JavaScript ローダー（iPhone/AR対応）
```

---

## 🚀 iPhone 17 Pro からのアクセス方法

### 1️⃣ **ローカル開発環境での動作確認**

```html
<!-- frontend/index.html -->
<script src="./static/registry-loader.js"></script>
<script>
  (async () => {
    const loader = RegistryLoader.getInstance();
    try {
      const registry = await loader.getRegistry();
      console.log("Registry loaded:", registry.meta);
      
      // 指定角度の山を取得
      const mountain = await loader.getMountainByDegree(45);
      console.log("Mountain at 45°:", mountain);
    } catch (error) {
      console.error("Error:", error);
    }
  })();
</script>
```

---

## 📦 fortune-core への統合手順

### **Step 1: ローカルコピー**

fortune-core リポジトリのルートに以下のファイルをコピー：

```bash
# fortune-core/ ディレクトリで実行
cp /path/to/fengshui-app/registry_a.py ./
cp /path/to/fengshui-app/registry_a.json ./
cp /path/to/fengshui-app/docs/registry_a.json ./docs/
cp /path/to/fengshui-app/static/registry-loader.js ./static/registry-loader.js
```

### **Step 2: GitHub Pages 設定**

fortune-core リポジトリの `docs/` フォルダに registry_a.json が配置されているため、以下の設定で自動公開：

1. GitHub リポジトリ設定 → **Pages** → **Source**
2. `Deploy from a branch` を選択
3. Branch: `main`、Folder: `/docs`

**公開 URL:**
```
https://norinori-jan.github.io/fortune-core/registry_a.json
```

### **Step 3: CORS 対応確認**

registry-loader.js は CORS モードで fetch するため、GitHub Pages は自動的に対応済み。

**テスト（iPhone Safari で実行）:**
```javascript
fetch("https://norinori-jan.github.io/fortune-core/registry_a.json", {
  mode: "cors"
})
.then(r => r.json())
.then(data => console.log("✅ CORS OK", data.meta))
.catch(e => console.error("❌ CORS Error", e));
```

---

## 🎯 今後のワークフロー

### **共通レジストリの更新フロー**

```
1. fengshui-app/core_logic.py で定義を更新
   ↓
2. registry_a.py を実行 → registry_a.json を再生成
   python registry_a.py
   ↓
3. fengshui-app リポジトリへ commit & push
   git add registry_a.json
   git commit -m "Update registry definitions"
   git push
   ↓
4. fortune-core へ registry_a.json をコピー
   cp registry_a.json ../fortune-core/registry_a.json
   cp registry_a.json ../fortune-core/docs/registry_a.json
   ↓
5. fortune-core リポジトリへ commit & push
   git add docs/registry_a.json
   git commit -m "Sync registry from fengshui-app"
   git push
   ↓
6. GitHub Pages 自動デプロイ完了
   → 全 UI が自動で最新データを fetch
```

---

## 📱 マルチプラットフォーム対応

### **JavaScript での使用**

```javascript
// Web App
import RegistryLoader from './static/registry-loader.js';

// or via CDN
const src = 'https://norinori-jan.github.io/fortune-core/static/registry-loader.js';
```

### **TypeScript での使用**

```typescript
// frontend/src/registry/registry.loader.ts
import RegistryLoader from '../static/registry-loader.js';

const loader = RegistryLoader.getInstance();
const mountain = await loader.getMountainByDegree(compassBearing);
```

### **Three.js / AR ゴーグル対応**

```javascript
// Quaternion 生成（ARグラスのジャイロ対応）
const quat = loader.getDirectionQuaternion(compassBearing);
// [x, y, z, w] → Three.js Quaternion へ直接代入可能
const quaternion = new THREE.Quaternion(...quat);
```

---

## 🔄 キャッシング戦略

registry-loader.js は自動的に以下のキャッシング を実装：

| 機能 | 設定値 | 説明 |
|------|--------|------|
| TTL | 24 時間 | 1 日ごとに最新データを fetch |
| 判定方法 | ETag対応 | HTTP 304 で効率化 |
| フォールバック | 複数URL | ローカル → GitHub Pages の順序 |

**キャッシュ無効化（強制更新）:**

```javascript
const loader = RegistryLoader.getInstance();
loader.clearCache(); // キャッシュ削除
const registry = await loader.getRegistry(true); // 強制リロード
```

---

## 📊 Registry 統計

```
{
  "version": "1.0.0",
  "last_updated": "2026-04-26T10:28:43.318812",
  
  "statistics": {
    "twenty_four_mountains": 24,
    "bagua": 8,
    "five_elements": 5,
    "heavenly_stems": 10,
    "earthly_branches": 12,
    "lopan_layers": 13,
    "total_definitions": 72,
    "file_size_bytes": 17040,
    "supported_platforms": ["web", "mobile_ios_17", "mobile_android", "ar_goggle"]
  }
}
```

---

## ✨ 次のステップ（UI 開発向け）

- [ ] fenshui_map で registry.loader を統合
- [ ] fengshui-app frontend で registry を参照
- [ ] Three.js で羅盤の 3D レンダリング
- [ ] iPhone Safari での AR 表示テスト
- [ ] AR ゴーグル（Apple Vision Pro 等）対応

---

**生成日時:** 2026-04-26
**スキーマバージョン:** 1.0.0
