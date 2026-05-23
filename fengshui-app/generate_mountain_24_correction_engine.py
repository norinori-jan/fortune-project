#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
地盤二十四山の補正値計算スクリプト
104分割グリッドでの24山の正確な補正値を計算
"""

import json
import math

def calculate_mountain_24_corrections():
    """
    地盤二十四山の補正値を計算
    24山の理想位置と104分割での実際位置の差を求める
    """

    CELL_WIDTH = 360.0 / 104  # 3.4615384615度
    corrections = []

    # 24山の理想位置（0°から始まり15°間隔）
    for mountain_id in range(1, 25):
        ideal_angle = (mountain_id - 1) * 15.0

        # 104分割での最も近いセル位置
        cell_index = round(ideal_angle / CELL_WIDTH)
        actual_angle = cell_index * CELL_WIDTH

        # 補正値（理想 - 実際）
        correction = ideal_angle - actual_angle

        # 正規化（-180°～180°の範囲に収める）
        while correction > 180:
            correction -= 360
        while correction < -180:
            correction += 360

        corrections.append({
            "id": mountain_id,
            "ideal": round(ideal_angle, 4),
            "actual": round(actual_angle, 4),
            "correction": round(correction, 4),
            "cell_index": cell_index
        })

    return corrections

def generate_mountain_24_json():
    """24山の補正データをJSON形式で生成"""

    corrections = calculate_mountain_24_corrections()

    # ユーザーのリクエスト形式に合わせたJSON
    result = {
        "layer": "地盤二十四山",
        "base_division": 104,
        "target_division": 24,
        "corrections": [
            {
                "index": corr["cell_index"],
                "offset_deg": corr["correction"]
            }
            for corr in corrections
        ]
    }

    return result

def generate_javascript_engine():
    """完全なJavaScript補正エンジンを生成"""

    corrections = calculate_mountain_24_corrections()

    # JSONデータをJavaScriptの定数として埋め込み
    corrections_json = json.dumps({
        "mountain_24": corrections
    }, ensure_ascii=False, indent=2)

    js_code = f"""// ============================================================================
// LopanCorrectionEngine.js - 地盤二十四山補正エンジン
// ============================================================================
// 104分割羅盤の地盤二十四山層に対する補正計算エンジン
// 生成日: 2026-04-18
// バージョン: 1.1

class LopanCorrectionEngine {{
    constructor() {{
        // 基本定数
        this.BASE_DIVISION = 104;
        this.CELL_WIDTH = 360.0 / this.BASE_DIVISION;

        // 補正データ（自動生成）
        this.CORRECTIONS = {corrections_json};
    }}

    // ============================================================================
    // 基本計算メソッド
    // ============================================================================

    /**
     * 104分割のインデックスから基本角度を計算
     * @param {{number}} index - セルインデックス (0～103)
     * @returns {{number}} 基本角度 (0～360°)
     */
    static calculateBaseAngle(index) {{
        const CELL_WIDTH = 360.0 / 104;
        return (index * CELL_WIDTH) % 360.0;
    }}

    /**
     * インデックスとオフセットから実際の描画角度を計算
     * @param {{number}} index - セルインデックス (0～103)
     * @param {{number}} offsetDeg - 補正オフセット (度)
     * @returns {{number}} 補正後の角度 (0～360°)
     */
    static calculateAngle(index, offsetDeg) {{
        const baseAngle = LopanCorrectionEngine.calculateBaseAngle(index);
        const correctedAngle = baseAngle + offsetDeg;

        // 角度を0～360°の範囲に正規化
        return ((correctedAngle % 360) + 360) % 360;
    }}

    /**
     * 角度を正規化（0～360°の範囲に収める）
     * @param {{number}} angle - 正規化する角度
     * @returns {{number}} 正規化された角度
     */
    static normalizeAngle(angle) {{
        return ((angle % 360) + 360) % 360;
    }}

    // ============================================================================
    // 地盤二十四山専用メソッド
    // ============================================================================

    /**
     * 地盤二十四山の補正データを取得
     * @param {{number}} mountainId - 山のID (1～24)
     * @returns {{object|null}} 補正データ {{id, ideal, actual, correction, cell_index}}
     */
    getMountainCorrection(mountainId) {{
        const corrections = this.CORRECTIONS.mountain_24 || [];
        return corrections.find(m => m.id === mountainId) || null;
    }}

    /**
     * 地盤二十四山の理想角度を取得
     * @param {{number}} mountainId - 山のID (1～24)
     * @returns {{number}} 理想角度 (0～360°)
     */
    getIdealMountainAngle(mountainId) {{
        const correction = this.getMountainCorrection(mountainId);
        return correction ? correction.ideal : 0;
    }}

    /**
     * 地盤二十四山の104分割での実際角度を取得
     * @param {{number}} mountainId - 山のID (1～24)
     * @returns {{number}} 実際角度 (0～360°)
     */
    getActualMountainAngle(mountainId) {{
        const correction = this.getMountainCorrection(mountainId);
        return correction ? correction.actual : 0;
    }}

    /**
     * 地盤二十四山の補正値を取得
     * @param {{number}} mountainId - 山のID (1～24)
     * @returns {{number}} 補正値 (度)
     */
    getMountainCorrectionValue(mountainId) {{
        const correction = this.getMountainCorrection(mountainId);
        return correction ? correction.correction : 0;
    }}

    /**
     * セルインデックスから最も近い地盤二十四山を取得
     * @param {{number}} cellIndex - セルインデックス (0～103)
     * @returns {{object}} 最も近い山の情報
     */
    getNearestMountain(cellIndex) {{
        const cellAngle = LopanCorrectionEngine.calculateBaseAngle(cellIndex);
        let nearestMountain = null;
        let minDistance = 360;

        this.CORRECTIONS.mountain_24.forEach(mountain => {{
            const distance = Math.min(
                Math.abs(cellAngle - mountain.ideal),
                360 - Math.abs(cellAngle - mountain.ideal)
            );

            if (distance < minDistance) {{
                minDistance = distance;
                nearestMountain = {{
                    ...mountain,
                    distance: distance,
                    cellIndex: cellIndex,
                    cellAngle: cellAngle
                }};
            }}
        }});

        return nearestMountain;
    }}

    // ============================================================================
    // 描画支援メソッド
    // ============================================================================

    /**
     * SVGで地盤二十四山の補正線を描画
     * @param {{HTMLElement}} svgElement - SVG要素
     * @param {{number}} radiusOuter - 外側半径
     * @param {{number}} radiusInner - 内側半径
     */
    drawMountainCorrectionLines(svgElement, radiusOuter = 100, radiusInner = 90) {{
        const corrections = this.CORRECTIONS.mountain_24 || [];

        corrections.forEach(correction => {{
            if (Math.abs(correction.correction) > 0.01) {{ // 誤差が0.01度以上のみ表示
                const angle = correction.actual * (Math.PI / 180);

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
                line.setAttribute('class', 'mountain-correction-line');
                line.setAttribute('title', `山${{correction.id}}: 補正 ${{correction.correction > 0 ? '+' : ''}}${{correction.correction.toFixed(3)}}°`);

                svgElement.appendChild(line);
            }}
        }});
    }}

    /**
     * 地盤二十四山の補正情報をテーブル形式で生成
     * @returns {{string}} HTMLテーブル
     */
    generateMountainCorrectionTable() {{
        const corrections = this.CORRECTIONS.mountain_24 || [];
        let html = `
            <table border="1" style="border-collapse: collapse;">
                <tr style="background-color: #f0f0f0;">
                    <th style="padding: 8px;">山ID</th>
                    <th style="padding: 8px;">理想角度 (°)</th>
                    <th style="padding: 8px;">実装角度 (°)</th>
                    <th style="padding: 8px;">補正値 (°)</th>
                    <th style="padding: 8px;">セル位置</th>
                </tr>`;

        corrections.forEach(correction => {{
            const corrStr = correction.correction > 0 ? '+' : '';
            html += `
                <tr>
                    <td style="padding: 8px; text-align: center;">${{correction.id}}</td>
                    <td style="padding: 8px; text-align: right;">${{correction.ideal.toFixed(2)}}</td>
                    <td style="padding: 8px; text-align: right;">${{correction.actual.toFixed(4)}}</td>
                    <td style="padding: 8px; text-align: right; color: ${{correction.correction !== 0 ? 'red' : 'black'}};">${{corrStr}}${{correction.correction.toFixed(4)}}</td>
                    <td style="padding: 8px; text-align: center;">${{correction.cell_index}}</td>
                </tr>`;
        }});

        html += '</table>';
        return html;
    }}

    /**
     * 補正統計情報を取得
     * @returns {{object}} 統計情報
     */
    getCorrectionStatistics() {{
        const corrections = this.CORRECTIONS.mountain_24 || [];
        const correctionValues = corrections.map(c => Math.abs(c.correction));

        return {{
            total_mountains: corrections.length,
            max_correction: Math.max(...correctionValues),
            min_correction: Math.min(...correctionValues),
            avg_correction: correctionValues.reduce((a, b) => a + b, 0) / correctionValues.length,
            zero_corrections: corrections.filter(c => c.correction === 0).length,
            non_zero_corrections: corrections.filter(c => c.correction !== 0).length
        }};
    }}

    // ============================================================================
    // デバッグ・検証メソッド
    // ============================================================================

    /**
     * 補正値の検証（整合性チェック）
     * @returns {{boolean}} 検証結果
     */
    validateCorrections() {{
        const corrections = this.CORRECTIONS.mountain_24 || [];
        let isValid = true;
        const errors = [];

        corrections.forEach((correction, index) => {{
            // 基本的な範囲チェック
            if (correction.id < 1 || correction.id > 24) {{
                errors.push(`山ID ${{correction.id}} が範囲外 (1-24)`);
                isValid = false;
            }}

            // 角度の範囲チェック
            if (correction.ideal < 0 || correction.ideal >= 360) {{
                errors.push(`山${{correction.id}} の理想角度 ${{correction.ideal}} が範囲外 (0-360)`);
                isValid = false;
            }}

            if (correction.actual < 0 || correction.actual >= 360) {{
                errors.push(`山${{correction.id}} の実装角度 ${{correction.actual}} が範囲外 (0-360)`);
                isValid = false;
            }}

            // 補正値の妥当性チェック
            const expectedCorrection = correction.ideal - correction.actual;
            const normalizedExpected = LopanCorrectionEngine.normalizeAngle(expectedCorrection);
            const normalizedActual = LopanCorrectionEngine.normalizeAngle(correction.correction);

            if (Math.abs(normalizedExpected - normalizedActual) > 0.001) {{
                errors.push(`山${{correction.id}} の補正値が不正: 期待 ${{normalizedExpected.toFixed(4)}}, 実際 ${{normalizedActual.toFixed(4)}}`);
                isValid = false;
            }}
        }});

        if (!isValid) {{
            console.error('補正値検証エラー:', errors);
        }}

        return isValid;
    }}
}}

// ============================================================================
// 使用例
// ============================================================================

// 基本的な使用
const engine = new LopanCorrectionEngine();

// 山5 (75°) の補正情報を取得
const mountain5 = engine.getMountainCorrection(5);
console.log('山5の補正情報:', mountain5);

// セルインデックス 20 から最も近い山を取得
const nearest = engine.getNearestMountain(20);
console.log('セル20に最も近い山:', nearest);

// 補正統計を取得
const stats = engine.getCorrectionStatistics();
console.log('補正統計:', stats);

// 検証実行
const isValid = engine.validateCorrections();
console.log('補正値検証結果:', isValid ? '✓ OK' : '✗ NG');

// HTMLテーブル生成
const tableHtml = engine.generateMountainCorrectionTable();
document.getElementById('correction-table').innerHTML = tableHtml;

// SVG描画
const svg = document.getElementById('compass-svg');
engine.drawMountainCorrectionLines(svg, 100, 90);

export default LopanCorrectionEngine;
"""

    return js_code

# ============================================================================
# 実行
# ============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("地盤二十四山補正値計算エンジン生成")
    print("=" * 80)
    print()

    # 補正値計算
    corrections = calculate_mountain_24_corrections()
    print("計算された補正値 (24山):")
    print("ID | 理想角度 | 実装角度 | 補正値 | セル位置")
    print("-" * 50)
    for corr in corrections[:8]:  # 最初の8個を表示
        corr_str = f"{corr['correction']:+.4f}"
        print(f"{corr['id']:2d} | {corr['ideal']:8.2f} | {corr['actual']:9.4f} | {corr_str:7s} | {corr['cell_index']:3d}")

    if len(corrections) > 8:
        print("... (残り16個)")
    print()

    # JSON生成
    json_data = generate_mountain_24_json()
    with open("mountain_24_corrections.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print("✓ JSON保存: mountain_24_corrections.json")

    # JavaScriptエンジン生成
    js_code = generate_javascript_engine()
    with open("LopanCorrectionEngine_24mountain.js", "w", encoding="utf-8") as f:
        f.write(js_code)
    print("✓ JavaScriptエンジン生成: LopanCorrectionEngine_24mountain.js")
    print(f"  行数: {len(js_code.splitlines())}")

    print()
    print("=" * 80)
    print("生成物:")
    print("  1. mountain_24_corrections.json - 補正データ")
    print("  2. LopanCorrectionEngine_24mountain.js - 計算エンジン")
    print()
    print("使用方法:")
    print("  const engine = new LopanCorrectionEngine();")
    print("  const correction = engine.getMountainCorrection(5); // 山5の補正")
    print("  const angle = LopanCorrectionEngine.calculateAngle(20, 1.15); // 補正計算")
    print("=" * 80)
