// ============================================================================
// test_mountain_24_engine.js - 地盤二十四山補正エンジンテスト
// ============================================================================

import LopanCorrectionEngine from './LopanCorrectionEngine_24mountain.js';

console.log('=== 地盤二十四山補正エンジンテスト ===');

// エンジン初期化
const engine = new LopanCorrectionEngine();

console.log('\n1. 基本情報:');
console.log(`基本分割数: ${engine.BASE_DIVISION}`);
console.log(`セル幅: ${engine.CELL_WIDTH.toFixed(4)}°`);

console.log('\n2. 山5の補正情報:');
const mountain5 = engine.getMountainCorrection(5);
console.log(JSON.stringify(mountain5, null, 2));

console.log('\n3. 補正統計:');
const stats = engine.getCorrectionStatistics();
console.log(JSON.stringify(stats, null, 2));

console.log('\n4. 検証結果:');
const isValid = engine.validateCorrections();
console.log(`補正値検証: ${isValid ? '✓ OK' : '✗ NG'}`);

console.log('\n5. セルインデックス 20 の最近接山:');
const nearest = engine.getNearestMountain(20);
console.log(JSON.stringify(nearest, null, 2));

console.log('\n6. 角度計算テスト:');
const testIndex = 17; // 山5のセル位置
const baseAngle = LopanCorrectionEngine.calculateBaseAngle(testIndex);
const correction = engine.getMountainCorrectionValue(5);
const correctedAngle = LopanCorrectionEngine.calculateAngle(testIndex, correction);
console.log(`セル${testIndex} 基本角度: ${baseAngle.toFixed(4)}°`);
console.log(`山5補正値: ${correction.toFixed(4)}°`);
console.log(`補正後角度: ${correctedAngle.toFixed(4)}°`);

console.log('\n=== テスト完了 ===');