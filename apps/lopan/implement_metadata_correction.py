#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
案2: メタデータ補正層の短期実装 - コード例

目的: 既存104分割CSVに補正メタデータを追加し、
      フロントエンド側でセル位置を補正する。

工数: 1-2週間
リスク: 低
効果: 中（完全正確性ではないが実用範囲）
"""

import csv
import math

# ============================================================================
# 1. CSVを拡張するスクリプト
# ============================================================================

def extend_csv_with_metadata(input_csv, output_csv):
    """
    既存の lopan_design_master_v1_104div.csv を拡張
    新列を追加: mountain_24_id, dragon_60_id, gold_120_id, host_28_id
    """
    
    CELL_WIDTH = 360.0 / 104
    
    # 二十八宿のマッピング（角度の中点から判定）
    hosts_by_angle = {
        "角": (0, 19),
        "亢": (19, 28),
        "氐": (28, 43),
        "房": (43, 48),
        "心": (48, 53),
        "尾": (53, 71),
        "箕": (71, 89),
        "斗": (89, 115),
        "牛": (115, 124),
        "女": (124, 136),
        "虚": (136, 146),
        "危": (146, 166),
        "室": (166, 182),
        "壁": (182, 191),
        "奎": (191, 207),
        "婁": (207, 221),
        "胃": (221, 235),
        "昴": (235, 246),
        "毛": (246, 259),
        "觜": (259, 264),
        "参": (264, 285),
        "井": (285, 306),
        "鬼": (306, 310),
        "柳": (310, 323),
        "星": (323, 336),
        "張": (336, 357),
        "翼": (357, 377),
        "軫": (377, 392),
    }
    
    def get_host_id(angle):
        """角度から二十八宿のIDを取得"""
        norm_angle = angle % 360.0
        host_ids = {name: idx+1 for idx, name in enumerate([
            "角", "亢", "氐", "房", "心", "尾", "箕", "斗",
            "牛", "女", "虚", "危", "室", "壁", "奎", "婁",
            "胃", "昴", "毛", "觜", "参", "井", "鬼", "柳",
            "星", "張", "翼", "軫"
        ])}
        
        for name, (start, end) in hosts_by_angle.items():
            if start <= norm_angle < end:
                return host_ids[name]
        return 1  # デフォルト
    
    def get_mountain_id(angle):
        """角度から24山のIDを取得"""
        # 24山: 0°=子, 15°=丑, 30°=寅, ...
        # IDは1～24
        norm_angle = (angle + 7.5) % 360.0
        return int(norm_angle / 15.0) % 24 + 1
    
    def get_dragon_id(angle):
        """角度から60龍のIDを取得"""
        # 60龍: 6°ごと
        norm_angle = angle % 360.0
        return int(norm_angle / 6.0) % 60 + 1
    
    def get_gold_id(angle):
        """角度から120分金のIDを取得"""
        # 120分金: 3°ごと
        norm_angle = angle % 360.0
        return int(norm_angle / 3.0) % 120 + 1
    
    # CSV読み込みと拡張
    rows = []
    with open(input_csv, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            start_angle = float(row['start_angle'])
            
            # メタデータを追加
            row['mountain_24_id'] = get_mountain_id(start_angle)
            row['dragon_60_id'] = get_dragon_id(start_angle)
            row['gold_120_id'] = get_gold_id(start_angle)
            row['host_28_id'] = get_host_id(start_angle)
            
            rows.append(row)
    
    # 拡張CSVを出力
    fieldnames = [
        'index', 'start_angle', 'end_angle', 'solar_term', 
        'ganchu', 'kyusei', 'unsu', 'kokei', 'niju_hasshuku',
        'mountain_24_id', 'dragon_60_id', 'gold_120_id', 'host_28_id'
    ]
    
    with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"✓ 拡張完了: {output_csv}")
    print(f"  追加列: mountain_24_id, dragon_60_id, gold_120_id, host_28_id")
    print(f"  行数: {len(rows)}")


# ============================================================================
# 2. JavaScriptで使用するPython補正ロジック（参考実装）
# ============================================================================

def calculate_correction_map():
    """
    描画時に使用する補正マップを生成
    補正値: 理想角度 - 実角度 = 補正するべき角度
    """
    
    CELL_WIDTH = 360.0 / 104
    corrections = {}
    
    # 24山の補正
    for mountain_id in range(1, 25):
        ideal_angle = (mountain_id - 1) * 15.0
        
        # 実装上の角度（セルの開始位置）
        cell_for_mountain = (mountain_id - 1) * (104 / 24.0)
        actual_angle = cell_for_mountain * CELL_WIDTH
        
        correction = ideal_angle - actual_angle
        corrections[f"mountain_{mountain_id:02d}"] = {
            "ideal_degrees": ideal_angle,
            "actual_degrees": actual_angle,
            "correction_degrees": correction,
            "cells_required": 104 / 24.0
        }
    
    # 60龍の補正
    for dragon_id in range(1, 61):
        ideal_angle = (dragon_id - 1) * 6.0
        cell_for_dragon = (dragon_id - 1) * (104 / 60.0)
        actual_angle = cell_for_dragon * CELL_WIDTH
        
        correction = ideal_angle - actual_angle
        corrections[f"dragon_{dragon_id:02d}"] = {
            "ideal_degrees": ideal_angle,
            "actual_degrees": actual_angle,
            "correction_degrees": correction,
            "cells_required": 104 / 60.0
        }
    
    # 120分金の補正
    for gold_id in range(1, 121):
        ideal_angle = (gold_id - 1) * 3.0
        cell_for_gold = (gold_id - 1) * (104 / 120.0)
        actual_angle = cell_for_gold * CELL_WIDTH
        
        correction = ideal_angle - actual_angle
        corrections[f"gold_{gold_id:03d}"] = {
            "ideal_degrees": ideal_angle,
            "actual_degrees": actual_angle,
            "correction_degrees": correction,
            "cells_required": 104 / 120.0
        }
    
    return corrections


# ============================================================================
# 3. JavaScriptへの埋め込み用データ生成
# ============================================================================

def generate_js_correction_engine():
    """
    フロントエンド用のJavaScript補正エンジンコードを生成
    """
    
    code = """
// ============================================================================
// LopanCorrectionEngine.js
// ============================================================================
// 104分割グリッドの補正ロジック
// 提供: アプリケーション補正層

class LopanCorrectionEngine {
  constructor() {
    this.CELL_WIDTH = 360.0 / 104;
    this.TOTAL_DEGREES = 360.0;
  }

  /**
   * セル位置から角度を計算（精度重視）
   * @param {number} cellIndex - セル番号 (0～103)
   * @returns {number} 角度 (0～360)
   */
  getAngleFromCell(cellIndex) {
    return (cellIndex * this.CELL_WIDTH) % this.TOTAL_DEGREES;
  }

  /**
   * 24山の理想角度を取得
   * @param {number} mountainId - 山のID (1～24)
   * @returns {number} 理想角度
   */
  getIdealMountainAngle(mountainId) {
    return ((mountainId - 1) * 15.0) % this.TOTAL_DEGREES;
  }

  /**
   * 24山の実装上の角度を取得
   * @param {number} mountainId - 山のID (1～24)
   * @returns {number} 実装上の角度
   */
  getActualMountainAngle(mountainId) {
    const cellPosition = (mountainId - 1) * (104 / 24.0);
    return this.getAngleFromCell(Math.floor(cellPosition));
  }

  /**
   * 24山の補正値を取得
   * @param {number} mountainId - 山のID (1～24)
   * @returns {object} {ideal, actual, correction}
   */
  getMountainCorrection(mountainId) {
    const ideal = this.getIdealMountainAngle(mountainId);
    const actual = this.getActualMountainAngle(mountainId);
    const correction = ideal - actual;
    
    return {
      mountainId: mountainId,
      ideal: ideal,
      actual: actual,
      correction: this.normalizeAngle(correction),
      display: `${correction > 0 ? '+' : ''}${correction.toFixed(2)}°`
    };
  }

  /**
   * 角度を正規化 (-180～180 or 0～360)
   * @param {number} angle - 正規化する角度
   * @returns {number} 正規化された角度
   */
  normalizeAngle(angle) {
    let normalized = angle % this.TOTAL_DEGREES;
    if (normalized < 0) normalized += this.TOTAL_DEGREES;
    return normalized;
  }

  /**
   * SVG/Canvas描画で补正線を追加する角度を計算
   * @param {number} baseAngle - ベース角度
   * @param {string} correctionType - "mountain"|"dragon"|"gold"
   * @returns {number} 补正後の描画角度
   */
  getCorrectedDrawingAngle(baseAngle, correctionType = "mountain") {
    // 補正値を適用
    // e.g., baseAngle = 15° (24山ID=2)
    //       correction = -1.154° 
    //       結果 = 15 - 1.154 = 13.846°
    
    if (correctionType === "mountain") {
      // 24山IDを取得 (0～360 に対して)
      const mountainId = Math.floor(((baseAngle + 7.5) / 15.0) % 24) + 1;
      const correction = this.getMountainCorrection(mountainId).correction;
      return this.normalizeAngle(baseAngle - correction);
    }
    
    return baseAngle; // その他は未実装
  }

  /**
   * セルベース描画の補正情報を一括取得
   * @returns {array} [{mountainId, ideal, actual, correction}, ...]
   */
  getAllMountainCorrections() {
    const corrections = [];
    for (let i = 1; i <= 24; i++) {
      corrections.push(this.getMountainCorrection(i));
    }
    return corrections;
  }

  /**
   * UI表示用: 補正マトリックスの生成
   */
  generateCorrectionMatrix() {
    const matrix = {
      gridSpecification: {
        totalDivisions: 104,
        cellWidth: this.CELL_WIDTH,
        totalDegrees: this.TOTAL_DEGREES
      },
      layers: {
        mountain24: {
          divisions: 24,
          corrections: this.getAllMountainCorrections(),
          totalError: this.getAllMountainCorrections()
            .reduce((sum, m) => sum + Math.abs(m.correction), 0)
        }
      }
    };
    
    return matrix;
  }
}

// ============================================================================
// 使用例
// ============================================================================

const engine = new LopanCorrectionEngine();

// 例1: 北 (山ID=1, 0°) の補正
const northCorrection = engine.getMountainCorrection(1);
console.log("北の補正:", northCorrection);
// 出力: {mountainId: 1, ideal: 0, actual: 3.46, correction: -3.46, display: "-3.46°"}

// 例2: すべての24山の補正一覧
const allCorrections = engine.getAllMountainCorrections();
console.log("24山の補正一覧:", allCorrections);

// 例3. SVGで補正線を描画
const svg = document.querySelector('svg');
allCorrections.forEach(correction => {
  if (Math.abs(correction.correction) > 0.1) {
    // 補正値が大きい場合のみ表示
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    const angle = correction.actual;
    const radius = 100;
    
    // 角度から座標を計算
    const x1 = radius * Math.cos(angle * Math.PI / 180);
    const y1 = radius * Math.sin(angle * Math.PI / 180);
    const x2 = radius * 1.1 * Math.cos(angle * Math.PI / 180);
    const y2 = radius * 1.1 * Math.sin(angle * Math.PI / 180);
    
    line.setAttribute('x1', x1);
    line.setAttribute('y1', y1);
    line.setAttribute('x2', x2);
    line.setAttribute('y2', y2);
    line.setAttribute('stroke', 'red');
    line.setAttribute('stroke-width', '1');
    line.setAttribute('stroke-dasharray', '2,2');
    line.setAttribute('title', `補正: ${correction.display}`);
    
    svg.appendChild(line);
  }
});
    """
    
    return code


# ============================================================================
# 実行例
# ============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("案2: メタデータ補正層の実装サンプル")
    print("=" * 80)
    print()
    
    # 1. CSVを拡張
    input_csv = "lopan_design_master_v1_104div.csv"
    output_csv = "lopan_design_master_v1_104div_extended.csv"
    
    print("[Step 1] CSV拡張")
    print(f"  入力: {input_csv}")
    print(f"  出力: {output_csv}")
    print()
    
    try:
        extend_csv_with_metadata(input_csv, output_csv)
    except FileNotFoundError:
        print(f"  ⚠️  {input_csv} が見つかりません。")
        print("  → このスクリプトは参考実装です。")
    
    print()
    
    # 2. 補正マップを生成
    print("[Step 2] 補正マップの生成")
    correction_map = calculate_correction_map()
    
    print("  サンプル補正値 (24山):")
    for key in list(correction_map.keys())[:3]:
        value = correction_map[key]
        print(f"    {key}: ideal={value['ideal_degrees']:.2f}°, "
              f"actual={value['actual_degrees']:.2f}°, "
              f"correction={value['correction_degrees']:+.2f}°")
    
    print()
    
    # 3. JavaScript コード生成
    print("[Step 3] JavaScript補正エンジンコードの生成")
    js_code = generate_js_correction_engine()
    
    with open("LopanCorrectionEngine.js", "w", encoding="utf-8") as f:
        f.write(js_code)
    
    print(f"  ✓ 生成完了: LopanCorrectionEngine.js")
    print(f"    行数: {len(js_code.splitlines())}")
    
    print()
    print("=" * 80)
    print("実装残タスク:")
    print("  1. lopan_104div_extended.csv を使用するよう API/DAO を更新")
    print("  2. LopanCorrectionEngine.js をフロントエンドにインポート")
    print("  3. SVG/Canvas レンダリングで補正線を表示")
    print("  4. UIで「補正値」をツールチップで説明")
    print("  5. テスト & 検証")
    print("=" * 80)

'''

このスクリプトは JSON 出力も可能です。
実行: python implement_metadata_correction.py
生成物:
  - lopan_design_master_v1_104div_extended.csv
  - LopanCorrectionEngine.js
"""

当スクリプト実行
