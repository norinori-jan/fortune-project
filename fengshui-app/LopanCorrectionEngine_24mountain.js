// ============================================================================
// LopanCorrectionEngine.js - 地盤二十四山補正エンジン
// ============================================================================
// 104分割羅盤の地盤二十四山層に対する補正計算エンジン
// 生成日: 2026-04-18
// バージョン: 1.1

class LopanCorrectionEngine {
    constructor() {
        // 基本定数
        this.BASE_DIVISION = 104;
        this.CELL_WIDTH = 360.0 / this.BASE_DIVISION;

        // 補正データ（自動生成）
        this.CORRECTIONS = {
  "mountain_24": [
    {
      "id": 1,
      "ideal": 0.0,
      "actual": 0.0,
      "correction": 0.0,
      "cell_index": 0
    },
    {
      "id": 2,
      "ideal": 15.0,
      "actual": 13.8462,
      "correction": 1.1538,
      "cell_index": 4
    },
    {
      "id": 3,
      "ideal": 30.0,
      "actual": 31.1538,
      "correction": -1.1538,
      "cell_index": 9
    },
    {
      "id": 4,
      "ideal": 45.0,
      "actual": 45.0,
      "correction": 0.0,
      "cell_index": 13
    },
    {
      "id": 5,
      "ideal": 60.0,
      "actual": 58.8462,
      "correction": 1.1538,
      "cell_index": 17
    },
    {
      "id": 6,
      "ideal": 75.0,
      "actual": 76.1538,
      "correction": -1.1538,
      "cell_index": 22
    },
    {
      "id": 7,
      "ideal": 90.0,
      "actual": 90.0,
      "correction": 0.0,
      "cell_index": 26
    },
    {
      "id": 8,
      "ideal": 105.0,
      "actual": 103.8462,
      "correction": 1.1538,
      "cell_index": 30
    },
    {
      "id": 9,
      "ideal": 120.0,
      "actual": 121.1538,
      "correction": -1.1538,
      "cell_index": 35
    },
    {
      "id": 10,
      "ideal": 135.0,
      "actual": 135.0,
      "correction": 0.0,
      "cell_index": 39
    },
    {
      "id": 11,
      "ideal": 150.0,
      "actual": 148.8462,
      "correction": 1.1538,
      "cell_index": 43
    },
    {
      "id": 12,
      "ideal": 165.0,
      "actual": 166.1538,
      "correction": -1.1538,
      "cell_index": 48
    },
    {
      "id": 13,
      "ideal": 180.0,
      "actual": 180.0,
      "correction": 0.0,
      "cell_index": 52
    },
    {
      "id": 14,
      "ideal": 195.0,
      "actual": 193.8462,
      "correction": 1.1538,
      "cell_index": 56
    },
    {
      "id": 15,
      "ideal": 210.0,
      "actual": 211.1538,
      "correction": -1.1538,
      "cell_index": 61
    },
    {
      "id": 16,
      "ideal": 225.0,
      "actual": 225.0,
      "correction": 0.0,
      "cell_index": 65
    },
    {
      "id": 17,
      "ideal": 240.0,
      "actual": 238.8462,
      "correction": 1.1538,
      "cell_index": 69
    },
    {
      "id": 18,
      "ideal": 255.0,
      "actual": 256.1538,
      "correction": -1.1538,
      "cell_index": 74
    },
    {
      "id": 19,
      "ideal": 270.0,
      "actual": 270.0,
      "correction": 0.0,
      "cell_index": 78
    },
    {
      "id": 20,
      "ideal": 285.0,
      "actual": 283.8462,
      "correction": 1.1538,
      "cell_index": 82
    },
    {
      "id": 21,
      "ideal": 300.0,
      "actual": 301.1538,
      "correction": -1.1538,
      "cell_index": 87
    },
    {
      "id": 22,
      "ideal": 315.0,
      "actual": 315.0,
      "correction": 0.0,
      "cell_index": 91
    },
    {
      "id": 23,
      "ideal": 330.0,
      "actual": 328.8462,
      "correction": 1.1538,
      "cell_index": 95
    },
    {
      "id": 24,
      "ideal": 345.0,
      "actual": 346.1538,
      "correction": -1.1538,
      "cell_index": 100
    }
  ]
};
    }

    // ============================================================================
    // 基本計算メソッド
    // ============================================================================

    /**
     * 104分割のインデックスから基本角度を計算
     * @param {number} index - セルインデックス (0～103)
     * @returns {number} 基本角度 (0～360°)
     */
    static calculateBaseAngle(index) {
        const CELL_WIDTH = 360.0 / 104;
        return (index * CELL_WIDTH) % 360.0;
    }

    /**
     * インデックスとオフセットから実際の描画角度を計算
     * @param {number} index - セルインデックス (0～103)
     * @param {number} offsetDeg - 補正オフセット (度)
     * @returns {number} 補正後の角度 (0～360°)
     */
    static calculateAngle(index, offsetDeg) {
        const baseAngle = LopanCorrectionEngine.calculateBaseAngle(index);
        const correctedAngle = baseAngle + offsetDeg;

        // 角度を0～360°の範囲に正規化
        return ((correctedAngle % 360) + 360) % 360;
    }

    /**
     * 角度を正規化（0～360°の範囲に収める）
     * @param {number} angle - 正規化する角度
     * @returns {number} 正規化された角度
     */
    static normalizeAngle(angle) {
        return ((angle % 360) + 360) % 360;
    }

    // ============================================================================
    // 地盤二十四山専用メソッド
    // ============================================================================

    /**
     * 地盤二十四山の補正データを取得
     * @param {number} mountainId - 山のID (1～24)
     * @returns {object|null} 補正データ {id, ideal, actual, correction, cell_index}
     */
    getMountainCorrection(mountainId) {
        const corrections = this.CORRECTIONS.mountain_24 || [];
        return corrections.find(m => m.id === mountainId) || null;
    }

    /**
     * 地盤二十四山の理想角度を取得
     * @param {number} mountainId - 山のID (1～24)
     * @returns {number} 理想角度 (0～360°)
     */
    getIdealMountainAngle(mountainId) {
        const correction = this.getMountainCorrection(mountainId);
        return correction ? correction.ideal : 0;
    }

    /**
     * 地盤二十四山の104分割での実際角度を取得
     * @param {number} mountainId - 山のID (1～24)
     * @returns {number} 実際角度 (0～360°)
     */
    getActualMountainAngle(mountainId) {
        const correction = this.getMountainCorrection(mountainId);
        return correction ? correction.actual : 0;
    }

    /**
     * 地盤二十四山の補正値を取得
     * @param {number} mountainId - 山のID (1～24)
     * @returns {number} 補正値 (度)
     */
    getMountainCorrectionValue(mountainId) {
        const correction = this.getMountainCorrection(mountainId);
        return correction ? correction.correction : 0;
    }

    /**
     * セルインデックスから最も近い地盤二十四山を取得
     * @param {number} cellIndex - セルインデックス (0～103)
     * @returns {object} 最も近い山の情報
     */
    getNearestMountain(cellIndex) {
        const cellAngle = LopanCorrectionEngine.calculateBaseAngle(cellIndex);
        let nearestMountain = null;
        let minDistance = 360;

        this.CORRECTIONS.mountain_24.forEach(mountain => {
            const distance = Math.min(
                Math.abs(cellAngle - mountain.ideal),
                360 - Math.abs(cellAngle - mountain.ideal)
            );

            if (distance < minDistance) {
                minDistance = distance;
                nearestMountain = {
                    ...mountain,
                    distance: distance,
                    cellIndex: cellIndex,
                    cellAngle: cellAngle
                };
            }
        });

        return nearestMountain;
    }

    // ============================================================================
    // 描画支援メソッド
    // ============================================================================

    /**
     * SVGで地盤二十四山の補正線を描画
     * @param {HTMLElement} svgElement - SVG要素
     * @param {number} radiusOuter - 外側半径
     * @param {number} radiusInner - 内側半径
     */
    drawMountainCorrectionLines(svgElement, radiusOuter = 100, radiusInner = 90) {
        const corrections = this.CORRECTIONS.mountain_24 || [];

        corrections.forEach(correction => {
            if (Math.abs(correction.correction) > 0.01) { // 誤差が0.01度以上のみ表示
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
                line.setAttribute('title', `山${correction.id}: 補正 ${correction.correction > 0 ? '+' : ''}${correction.correction.toFixed(3)}°`);

                svgElement.appendChild(line);
            }
        });
    }

    /**
     * 地盤二十四山の補正情報をテーブル形式で生成
     * @returns {string} HTMLテーブル
     */
    generateMountainCorrectionTable() {
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

        corrections.forEach(correction => {
            const corrStr = correction.correction > 0 ? '+' : '';
            html += `
                <tr>
                    <td style="padding: 8px; text-align: center;">${correction.id}</td>
                    <td style="padding: 8px; text-align: right;">${correction.ideal.toFixed(2)}</td>
                    <td style="padding: 8px; text-align: right;">${correction.actual.toFixed(4)}</td>
                    <td style="padding: 8px; text-align: right; color: ${correction.correction !== 0 ? 'red' : 'black'};">${corrStr}${correction.correction.toFixed(4)}</td>
                    <td style="padding: 8px; text-align: center;">${correction.cell_index}</td>
                </tr>`;
        });

        html += '</table>';
        return html;
    }

    /**
     * 補正統計情報を取得
     * @returns {object} 統計情報
     */
    getCorrectionStatistics() {
        const corrections = this.CORRECTIONS.mountain_24 || [];
        const correctionValues = corrections.map(c => Math.abs(c.correction));

        return {
            total_mountains: corrections.length,
            max_correction: Math.max(...correctionValues),
            min_correction: Math.min(...correctionValues),
            avg_correction: correctionValues.reduce((a, b) => a + b, 0) / correctionValues.length,
            zero_corrections: corrections.filter(c => c.correction === 0).length,
            non_zero_corrections: corrections.filter(c => c.correction !== 0).length
        };
    }

    // ============================================================================
    // デバッグ・検証メソッド
    // ============================================================================

    /**
     * 補正値の検証（整合性チェック）
     * @returns {boolean} 検証結果
     */
    validateCorrections() {
        const corrections = this.CORRECTIONS.mountain_24 || [];
        let isValid = true;
        const errors = [];

        corrections.forEach((correction, index) => {
            // 基本的な範囲チェック
            if (correction.id < 1 || correction.id > 24) {
                errors.push(`山ID ${correction.id} が範囲外 (1-24)`);
                isValid = false;
            }

            // 角度の範囲チェック
            if (correction.ideal < 0 || correction.ideal >= 360) {
                errors.push(`山${correction.id} の理想角度 ${correction.ideal} が範囲外 (0-360)`);
                isValid = false;
            }

            if (correction.actual < 0 || correction.actual >= 360) {
                errors.push(`山${correction.id} の実装角度 ${correction.actual} が範囲外 (0-360)`);
                isValid = false;
            }

            // 補正値の妥当性チェック
            const expectedCorrection = correction.ideal - correction.actual;
            const normalizedExpected = LopanCorrectionEngine.normalizeAngle(expectedCorrection);
            const normalizedActual = LopanCorrectionEngine.normalizeAngle(correction.correction);

            if (Math.abs(normalizedExpected - normalizedActual) > 0.001) {
                errors.push(`山${correction.id} の補正値が不正: 期待 ${normalizedExpected.toFixed(4)}, 実際 ${normalizedActual.toFixed(4)}`);
                isValid = false;
            }
        });

        if (!isValid) {
            console.error('補正値検証エラー:', errors);
        }

        return isValid;
    }
}

// ============================================================================
// 使用例 (ブラウザ環境でのみ実行)
// ============================================================================

// ブラウザ環境でのみ実行されるようにチェック
if (typeof window !== 'undefined' && typeof document !== 'undefined') {
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

    // HTMLテーブル生成（要素が存在する場合のみ）
    const tableElement = document.getElementById('correction-table');
    if (tableElement) {
        const tableHtml = engine.generateMountainCorrectionTable();
        tableElement.innerHTML = tableHtml;
    }

    // SVG描画（要素が存在する場合のみ）
    const svgElement = document.getElementById('compass-svg');
    if (svgElement) {
        engine.drawMountainCorrectionLines(svgElement, 100, 90);
    }
}

export default LopanCorrectionEngine;
