/**
 * 羅盤 統合テスト：補正エンジン + 全22層解析
 */
import LopanCorrectionEngine from './LopanCorrectionEngine_24mountain.js';
import { analyzeAllLayers } from './src/lopanDatabase.js';

const engine = new LopanCorrectionEngine();

/**
 * 補正後の解析結果を取得するラッパー関数
 */
const getCorrectedAnalysis = (rawDeg) => {
    // 1. 現在の角度に最も近い「二十四山」のIDを特定
    const nearest = engine.getNearestMountainFromAngle(rawDeg);
    
    // 2. その山に割り当てられた補正値(correction)を取得
    const correction = engine.getMountainCorrectionValue(nearest.id);
    
    // 3. 生の角度に補正を加えて「羅盤上の正解角度」を算出
    const correctedDeg = (rawDeg + correction + 360) % 360;

    // 4. 補正後の角度で全レイヤーをスキャン
    const results = analyzeAllLayers(correctedDeg);

    return {
        rawDeg: rawDeg.toFixed(2),
        correctedDeg: correctedDeg.toFixed(2),
        correction: correction.toFixed(4),
        nearestMountain: nearest.id,
        layers: results
    };
};

const runFullTest = () => {
    // 検証したい角度（北、山5付近、L14切り替わりなど）
    const testPoints = [0, 5.625, 15, 58.85, 60, 180, 359.9];

    console.log("=== 補正エンジン連動・全層整合性チェック ===");
    
    const tableData = testPoints.map(deg => {
        const data = getCorrectedAnalysis(deg);
        return {
            "入力角度": data.rawDeg + "°",
            "補正値": data.correction,
            "補正後": data.correctedDeg + "°",
            "L4(山ID)": data.layers.L4 || '-',
            "L14(八卦)": data.layers.L14 || '-',
            "L15(卦名)": data.layers.L15 || '-',
            "L16(九星)": data.layers.L16 || '-',
            "L22(分金)": data.layers.L22 || '未実装'
        };
    });

    console.table(tableData);

    console.log("\n--- 方位スキャン（補正の掛かり具合を確認） ---");
    for (let i = 0; i < 360; i += 30) {
        const data = getCorrectedAnalysis(i);
        console.log(
            `入力:${String(i).padStart(3)}° -> 補正後:${data.correctedDeg.padStart(6)}° ` +
            `| L15:${data.layers.L15 || '??'}`
        );
    }
};

try {
    runFullTest();
} catch (e) {
    console.error("【実行失敗】");
    console.error("原因:", e.message);
    console.log("\nヒント: analyzeAllLayers が export されているか、ファイルのパスが正しいか確認してください。");
}