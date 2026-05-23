#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
案2: メタデータ補正層の短期実装
104分割グリッドにメタデータを追加し、補正エンジンを生成
"""

import csv
import json

# ============================================================================
# Step 1: CSVを拡張
# ============================================================================

def extend_csv_with_metadata(input_csv, output_csv):
    """既存CSVにメタデータ列を追加"""
    
    CELL_WIDTH = 360.0 / 104
    
    def get_mountain_id(angle):
        """角度から24山のID (1～24) を取得"""
        norm_angle = (angle + 7.5) % 360.0
        return int(norm_angle / 15.0) % 24 + 1
    
    def get_dragon_id(angle):
        """角度から60龍のID (1～60) を取得"""
        norm_angle = angle % 360.0
        return int(norm_angle / 6.0) % 60 + 1
    
    def get_gold_id(angle):
        """角度から120分金のID (1～120) を取得"""
        norm_angle = angle % 360.0
        return int(norm_angle / 3.0) % 120 + 1
    
    # CSV読み込み
    rows = []
    with open(input_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            start_angle = float(row['start_angle'])
            
            # メタデータを追加
            row['mountain_24_id'] = int(get_mountain_id(start_angle))
            row['dragon_60_id'] = int(get_dragon_id(start_angle))
            row['gold_120_id'] = int(get_gold_id(start_angle))
            
            rows.append(row)
    
    # 拡張CSVを出力
    fieldnames = [
        'index', 'start_angle', 'end_angle', 'solar_term',
        'ganchu', 'kyusei', 'unsu', 'kokei', 'niju_hasshuku',
        'mountain_24_id', 'dragon_60_id', 'gold_120_id'
    ]
    
    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    return len(rows)


# ============================================================================
# Step 2: 補正マップを生成
# ============================================================================

def generate_correction_map():
    """補正値を計算"""
    
    CELL_WIDTH = 360.0 / 104
    corrections = {}
    
    # 24山の補正
    mountain_corrections = []
    for mountain_id in range(1, 25):
        ideal_angle = (mountain_id - 1) * 15.0
        cell_position = (mountain_id - 1) * (104 / 24.0)
        actual_angle = cell_position * CELL_WIDTH
        correction = ideal_angle - actual_angle
        
        mountain_corrections.append({
            "id": mountain_id,
            "ideal": round(ideal_angle, 4),
            "actual": round(actual_angle, 4),
            "correction": round(correction, 4)
        })
    
    corrections['mountain_24'] = mountain_corrections
    
    # 60龍の補正
    dragon_corrections = []
    for dragon_id in range(1, 61):
        ideal_angle = (dragon_id - 1) * 6.0
        cell_position = (dragon_id - 1) * (104 / 60.0)
        actual_angle = cell_position * CELL_WIDTH
        correction = ideal_angle - actual_angle
        
        dragon_corrections.append({
            "id": dragon_id,
            "ideal": round(ideal_angle, 4),
            "actual": round(actual_angle, 4),
            "correction": round(correction, 4)
        })
    
    corrections['dragon_60'] = dragon_corrections
    
    # 120分金の補正
    gold_corrections = []
    for gold_id in range(1, 121):
        ideal_angle = (gold_id - 1) * 3.0
        cell_position = (gold_id - 1) * (104 / 120.0)
        actual_angle = cell_position * CELL_WIDTH
        correction = ideal_angle - actual_angle
        
        gold_corrections.append({
            "id": gold_id,
            "ideal": round(ideal_angle, 4),
            "actual": round(actual_angle, 4),
            "correction": round(correction, 4)
        })
    
    corrections['gold_120'] = gold_corrections
    
    return corrections


# ============================================================================
# Step 3: JavaScriptエンジンを生成
# ============================================================================

def generate_js_engine():
    """JavaScript補正エンジンコードを生成"""
    
    code = """// LopanCorrectionEngine.js
// 104分割羅盤の補正ロジック

class LopanCorrectionEngine {
  constructor() {
    this.CELL_WIDTH = 360.0 / 104;
    this.CORRECTIONS = {}; // 実行時に外部から設定
  }
  
  /**
   * 24山の補正値を取得
   */
  getMountainCorrection(mountainId) {
    const corrections = this.CORRECTIONS['mountain_24'] || [];
    return corrections.find(m => m.id === mountainId) || null;
  }
  
  /**
   * CVSから読み込んだセルデータ + 補正を応用して描画
   */
  getCorrectedAngle(layerType, layerId) {
    const corrections = this.CORRECTIONS[layerType] || [];
    const item = corrections.find(obj => obj.id === layerId);
    return item ? item.actual : null;
  }
  
  /**
   * SVG描画時に補正線を追加
   */
  drawCorrectionLines(svgElement, layerType = 'mountain_24', radiusOuter = 100, radiusInner = 90) {
    const corrections = this.CORRECTIONS[layerType] || [];
    
    corrections.forEach(obj => {
      if (Math.abs(obj.correction) > 0.05) { // 誤差が0.05度以上のみ表示
        const angle = (obj.actual * Math.PI) / 180;
        
        const x1 = radiusInner * Math.cos(angle);
        const y1 = radiusInner * Math.sin(angle);
        const x2 = radiusOuter * Math.cos(angle);
        const y2 = radiusOuter * Math.sin(angle);
        
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', x1);
        line.setAttribute('y1', y1);
        line.setAttribute('x2', x2);
        line.setAttribute('y2', y2);
        line.setAttribute('stroke', 'red');
        line.setAttribute('stroke-width', '1');
        line.setAttribute('stroke-dasharray', '2,2');
        line.setAttribute('class', 'correction-line');
        line.setAttribute('title', `ID:${obj.id} 補正: ${obj.correction > 0 ? '+' : ''}${obj.correction.toFixed(3)}°`);
        
        svgElement.appendChild(line);
      }
    });
  }
  
  /**
   * テーブル形式で補正情報を表示
   */
  generateCorrectionTable(layerType = 'mountain_24') {
    const corrections = this.CORRECTIONS[layerType] || [];
    let html = '<table border="1"><tr><th>ID</th><th>理想(°)</th><th>実装(°)</th><th>補正(°)</th></tr>';
    
    corrections.forEach(obj => {
      const corrStr = obj.correction > 0 ? '+' : '';
      html += `<tr><td>${obj.id}</td><td>${obj.ideal.toFixed(2)}</td><td>${obj.actual.toFixed(2)}</td><td>${corrStr}${obj.correction.toFixed(4)}</td></tr>`;
    });
    
    html += '</table>';
    return html;
  }
}

// 使用例
// const engine = new LopanCorrectionEngine();
// engine.CORRECTIONS = correctionMapFromJSON; // サーバーから読み込み
// engine.drawCorrectionLines(svgElement, 'mountain_24');
"""
    
    return code


# ============================================================================
# 実行
# ============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("案2: メタデータ補正層 実装ツール")
    print("=" * 80)
    print()
    
    input_csv = "lopan_design_master_v1_104div.csv"
    output_csv = "lopan_design_master_v1_104div_extended.csv"
    
    # Step 1
    print("[Step 1] CSVにメタデータ列を追加中...")
    try:
        row_count = extend_csv_with_metadata(input_csv, output_csv)
        print(f"  ✓ 完了: {output_csv}")
        print(f"    行数: {row_count} + ヘッダー 1行")
    except FileNotFoundError as e:
        print(f"  ✗ エラー: {e}")
    
    print()
    
    # Step 2
    print("[Step 2] 補正マップを生成中...")
    corrections = generate_correction_map()
    
    # JSON保存
    json_file = "lopan_corrections.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(corrections, f, ensure_ascii=False, indent=2)
    print(f"  ✓ JSON保存: {json_file}")
    
    # サンプル表示
    print("\n  24山の補正値（サンプル）:")
    for m in corrections['mountain_24'][:5]:
        correction_str = f"{m['correction']:+.4f}"
        print(f"    ID {m['id']:2d}: 理想 {m['ideal']:7.2f}° → 実装 {m['actual']:7.4f}° "
              f"（補正: {correction_str}°）")
    
    print()
    
    # Step 3
    print("[Step 3] JavaScriptエンジンを生成中...")
    js_code = generate_js_engine()
    js_file = "LopanCorrectionEngine.js"
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(js_code)
    print(f"  ✓ 生成完了: {js_file}")
    print(f"    行数: {len(js_code.splitlines())}")
    
    print()
    print("=" * 80)
    print("✅ 実装準備完了")
    print()
    print("次のステップ:")
    print("  1. lopan_design_master_v1_104div_extended.csv をバックエンドで利用")
    print("  2. lopan_corrections.json をAPIで配信")
    print("  3. LopanCorrectionEngine.js をフロントエンドにインポート")
    print("  4. SVG/Canvas描画で補正線を表示")
    print("  5. UIで補正値をツールチップで説明")
    print("=" * 80)
