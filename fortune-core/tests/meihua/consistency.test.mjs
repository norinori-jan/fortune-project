import { computeBianGua, computeHuGua } from "../../src/meihua/bianGuaCalculator.js";
import { buildDanzi } from "../../src/meihua/meihuaEngine.js";
import { calcJudgeKey } from "../../src/meihua/calcJudgeKey.js";
import { getRelation, WUXING_SHENG, WUXING_KE } from "../../src/meihua/utils.js";
import { divinate } from "../../src/meihua/strategies/taiYiuStandard.js";
import dataRegistry from "../../src/meihua/registries/dataRegistry.js";

let pass = 0;
let fail = 0;
function check(label, actual, expected) {
  const ok = JSON.stringify(actual) === JSON.stringify(expected);
  if (ok) {
    pass++;
    console.log(`  ✅ ${label}`);
  } else {
    fail++;
    console.log(`  ❌ ${label}`);
    console.log(`     期待値: ${JSON.stringify(expected)}`);
    console.log(`     実際値: ${JSON.stringify(actual)}`);
  }
}

console.log("========================================");
console.log("1. bianGuaCalculator.js — 教科書的な既知の結果との一致");
console.log("========================================");
check("乾為天・初爻変 → 天風姤",
  computeBianGua("乾", "乾", 1),
  { upperName: "乾", lowerName: "巽", changedTrigram: "lower" });
check("地天泰(坤上乾下)・上爻変 → 山天大畜",
  computeBianGua("坤", "乾", 6),
  { upperName: "艮", lowerName: "乾", changedTrigram: "upper" });
check("地天泰(坤上乾下)・互卦 → 雷沢帰妹",
  computeHuGua("坤", "乾"),
  { upperName: "震", lowerName: "兌" });
try {
  computeBianGua("乾", "乾", 7);
  check("範囲外changingLineで例外", "例外なし(NG)", "例外あり");
} catch (e) {
  check("範囲外changingLineで例外", "例外あり", "例外あり");
}
try {
  computeBianGua("未知の卦", "乾", 1);
  check("未知の卦名で例外", "例外なし(NG)", "例外あり");
} catch (e) {
  check("未知の卦名で例外", "例外あり", "例外あり");
}

console.log();
console.log("========================================");
console.log("2. utils.js — 相生相克の全組み合わせ(5x5=25通り)");
console.log("========================================");
const ELEMENTS = ["木", "火", "土", "金", "水"];
let relationErrors = 0;
for (const a of ELEMENTS) {
  for (const b of ELEMENTS) {
    const rel = getRelation(a, b);
    let expected;
    if (a === b) expected = "比和";
    else if (WUXING_SHENG[a] === b) expected = "相生（生じる）";
    else if (WUXING_SHENG[b] === a) expected = "相生（生まれる）";
    else if (WUXING_KE[a] === b) expected = "相克（克する）";
    else if (WUXING_KE[b] === a) expected = "相克（克される）";
    if (rel !== expected) {
      relationErrors++;
      console.log(`  ❌ getRelation(${a},${b}) = ${rel} (期待: ${expected})`);
    }
  }
}
check("25通り全て自己無矛盾", relationErrors, 0);

console.log();
console.log("========================================");
console.log("3. meihuaEngine.js と calcJudgeKey.js の整合性");
console.log("   （同じ本卦・同じ変爻を与えたとき、体用の五行が完全一致するか）");
console.log("========================================");
const testCases = [
  { upperName: "坤", lowerName: "乾", changingLine: 6, label: "地天泰・上爻変" },
  { upperName: "乾", lowerName: "乾", changingLine: 1, label: "乾為天・初爻変" },
  { upperName: "乾", lowerName: "乾", changingLine: 4, label: "乾為天・四爻変" },
  { upperName: "離", lowerName: "坎", changingLine: 3, label: "水火既済(仮)・三爻変" },
  { upperName: "震", lowerName: "巽", changingLine: 2, label: "風雷益(仮)・二爻変" },
];
for (const tc of testCases) {
  const engineResult = buildDanzi({
    upperName: tc.upperName, lowerName: tc.lowerName, changingLine: tc.changingLine,
    monthBranch: "子", dayBranch: "子",
  });
  const judgeResult = calcJudgeKey({
    benGua: { trigram_upper: tc.upperName, trigram_lower: tc.lowerName },
    changingLine: tc.changingLine,
    domain: "test", timestamp: new Date().toISOString(),
  });
  check(`${tc.label}: tai`, judgeResult.tai, engineResult.details.tai);
  check(`${tc.label}: you`, judgeResult.you, engineResult.details.you);
  check(`${tc.label}: tiWuxing/youWuxing`,
    { ti: judgeResult.tiWuxing, you: judgeResult.youWuxing },
    { ti: dataRegistry.getHexagram(engineResult.details.tai).wuxing,
      you: dataRegistry.getHexagram(engineResult.details.you).wuxing });
  check(`${tc.label}: zhiGua(変卦)の上卦・下卦`,
    { upper: judgeResult.zhiGua.upperName, lower: judgeResult.zhiGua.lowerName },
    (() => {
      const bian = computeBianGua(tc.upperName, tc.lowerName, tc.changingLine);
      return { upper: bian.upperName, lower: bian.lowerName };
    })()
  );
}

console.log();
console.log("========================================");
console.log("4. calcJudgeKey.js — changingLine未指定時のフォールバック");
console.log("========================================");
const fallback = calcJudgeKey({
  benGua: { trigram_upper: "坤", trigram_lower: "乾" },
  domain: "test", timestamp: new Date().toISOString(),
});
check("フォールバック: tai=上卦", fallback.tai, "坤");
check("フォールバック: you=下卦", fallback.you, "乾");
check("フォールバック: zhiGuaは計算されない(undefined)", fallback.zhiGua, undefined);

console.log();
console.log("========================================");
console.log("5. calcJudgeKey.js — 相剋(相克)判定が正しく動くか（文字コード修正の確認）");
console.log("========================================");
// 木克土: 木が体・土が用 → TAI_KOKU_YOU or TAI_STRONG_YOU_WEAK になるはず（MIXEDではダメ）
const kokuTest = calcJudgeKey({
  benGua: { trigram_upper: "震", trigram_lower: "艮" }, // 震=木(体・上卦), 艮=土(用・下卦), changingLine未指定→体=上卦
  domain: "test", timestamp: new Date().toISOString(),
});
const isMixed = kokuTest.relation === "MIXED";
check("木(体)克土(用)がMIXEDに落ちていない", isMixed, false);
console.log(`     実際のrelation: ${kokuTest.relation} (tiWuxing=${kokuTest.tiWuxing}, youWuxing=${kokuTest.youWuxing})`);

console.log();
console.log("========================================");
console.log("6. taiYiuStandard.js — 既存の独立関数が壊れていないか");
console.log("========================================");
const divResult = divinate({ upperName: "乾", lowerName: "坤", changingLine: 3 });
check("divinate()がエラーを返さない", !divResult.error, true);
check("divinate()の基本フィールド", 
  { upper: divResult.upper?.name, lower: divResult.lower?.name },
  { upper: "乾", lower: "坤" });

console.log();
console.log("========================================");
console.log(`結果: ${pass}件成功 / ${fail}件失敗`);
console.log("========================================");
process.exit(fail > 0 ? 1 : 0);
