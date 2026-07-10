import { getRelation } from "./utils.js";
import dataRegistry from "./registries/dataRegistry.js";
import { computeBianGua } from "./bianGuaCalculator.js";

// 時間スコープの判定
function judgeTimeScope(dateStr) {
  const now = new Date();
  const target = new Date(dateStr);
  const diffDays = (target - now) / (1000 * 60 * 60 * 24);
  if (Math.abs(diffDays) <= 31) return "THIS_MONTH";
  if (Math.abs(diffDays) <= 365) return "THIS_YEAR";
  return "NOW";
}

// 体と用の五行から relation キーを決定
// FIX: utils.js の getRelation() が実際に返すのは「相克」（克）だが、
//      ここでは異体字の「相剋」（剋）と比較しており、常に不一致でMIXEDに
//      落ちていた。utils.js側の実際の返り値に合わせて修正。
function judgeRelation(tiWuxing, youWuxing, tiStrength, youStrength) {
  if (tiWuxing === youWuxing) return "SAME_ELEMENT";

  const raw = getRelation(tiWuxing, youWuxing);

  if (raw === "相克（克する）") {
    return tiStrength > youStrength ? "TAI_STRONG_YOU_WEAK" : "TAI_KOKU_YOU";
  }
  if (raw === "相克（克される）") {
    return youStrength > tiStrength ? "YOU_STRONG_TAI_WEAK" : "YOU_KOKU_TAI";
  }
  if (raw === "相生（生じる）") return "TAI_SEI_YOU";
  if (raw === "相生（生まれる）") return "YOU_SEI_TAI";
  return "MIXED";
}

/**
 * メイン関数
 *
 * FIX: 「体＝上卦固定」だった不具合を修正。meihuaEngine.js と同じルールで、
 *      体＝変爻を含まない方の卦、用＝変爻を含む方の卦とする。
 * FIX: 之卦(zhiGua)を外部から受け取る設計をやめ、bianGuaCalculator.js で
 *      内部計算するように変更（meihuaEngine.js とロジックを共有し、
 *      二重実装によるズレを防ぐため）。
 *
 * ⚠️ 破壊的変更: 旧シグネチャは { benGua, zhiGua, domain, timestamp } だったが、
 *    新シグネチャは { benGua, changingLine, domain, timestamp }。
 *    zhiGua を渡していた既存の呼び出し元があれば、changingLine を渡す形に
 *    直す必要がある。
 *
 * @param {Object} params
 * @param {{trigram_upper: string, trigram_lower: string}} params.benGua - 本卦
 * @param {number} [params.changingLine] - 変爻の位置（1〜6）。未指定の場合は
 *        後方互換のため「体＝上卦」にフォールバックする。
 * @param {string} params.domain
 * @param {string} params.timestamp
 * @returns {{
 *   relation: string, domain: string, timeScope: string,
 *   tiWuxing: string, youWuxing: string,
 *   tai: string, you: string,
 *   zhiGua?: { upperName: string, lowerName: string, changedTrigram: 'upper'|'lower' }
 * } | null}
 */
export function calcJudgeKey({ benGua, changingLine, domain, timestamp }) {
  const upper = dataRegistry.getHexagram(benGua.trigram_upper);
  const lower = dataRegistry.getHexagram(benGua.trigram_lower);

  if (!upper || !lower) return null;

  // 体用の決定（梅花易数の基本ルール。meihuaEngine.js の buildDanzi と同一ロジック）
  const hasValidChangingLine =
    Number.isInteger(changingLine) && changingLine >= 1 && changingLine <= 6;
  const lineIsInUpper = hasValidChangingLine && changingLine >= 4;
  const taiIsUpper = hasValidChangingLine ? !lineIsInUpper : true; // フォールバック: 体=上卦

  const tiWuxing = taiIsUpper ? upper.wuxing : lower.wuxing;
  const youWuxing = taiIsUpper ? lower.wuxing : upper.wuxing;

  // 強さは卦番号（先天八卦数）で簡易代用（後で命式計算に差し替え可）
  const tiStrength = taiIsUpper ? upper.number : lower.number;
  const youStrength = taiIsUpper ? lower.number : upper.number;

  const relation = judgeRelation(tiWuxing, youWuxing, tiStrength, youStrength);
  const timeScope = judgeTimeScope(timestamp);

  const result = {
    relation,
    domain,
    timeScope,
    tiWuxing,
    youWuxing,
    tai: taiIsUpper ? benGua.trigram_upper : benGua.trigram_lower,
    you: taiIsUpper ? benGua.trigram_lower : benGua.trigram_upper,
  };

  // 変爻が分かっていれば、変卦（之卦）も内部計算して結果に含める
  if (hasValidChangingLine) {
    const bian = computeBianGua(benGua.trigram_upper, benGua.trigram_lower, changingLine);
    result.zhiGua = {
      upperName: bian.upperName,
      lowerName: bian.lowerName,
      changedTrigram: bian.changedTrigram,
    };
  }

  return result;
}
