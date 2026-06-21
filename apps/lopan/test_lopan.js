/**
 * 羅盤 全22層 整合性チェック用テストスクリプト
 */
// 拡張子が .js かつ type: module の場合は import、それ以外は共通ファイルに追記を推奨
import { analyzeAllLayers } from './src/lopanDatabase.js'; 

const verifyLopanLayers = () => {
    const testDegrees = [0, 5.625, 11.25, 15, 45, 180, 354.375, 359.9];

    console.log("--- 特定角度の整合性チェック ---");
    console.table(testDegrees.map(deg => {
        const results = analyzeAllLayers(deg);
        return {
            "角度": deg + "°",
            "L4(二十四山)": results.L4 || '未実装', 
            "L14(八卦)": results.L14 || '未実装',
            "L15(卦名)": results.L15 || '未実装',
            "L16(九星)": results.L16 || '未実装',
            "L22(分金)": results.L22 || '未実装/計算中'
        };
    }));

    console.log("--- 連続スキャン（15度刻み） ---");
    for (let i = 0; i < 360; i += 15) {
        const res = analyzeAllLayers(i);
        // バッククォートを使わない安全な記述に変更
        console.log("[" + String(i).padStart(3, ' ') + "°] L4:" + (res.L4 || '??') + " | L15:" + (res.L15 || '??'));
    }
};

try {
    verifyLopanLayers();
} catch (e) {
    console.error("実行エラー:");
    console.error(e.message);
}