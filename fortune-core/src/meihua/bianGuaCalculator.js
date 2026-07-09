/**
 * bianGuaCalculator.js
 *
 * 梅花心易における「変卦」（へんか）と「互卦」（ごか）を、
 * 古典易学の定義に基づいて計算する。
 *
 * ── 六爻の並び（下から上へ） ──
 *   爻1・爻2・爻3 = 下卦（内卦）
 *   爻4・爻5・爻6 = 上卦（外卦）
 *
 * ── 八卦の陰陽構成（下から上へ、1=陽・0=陰） ──
 *   乾 111   兌 110   離 101   震 100
 *   巽 011   坎 010   艮 001   坤 000
 *
 * 変卦: 指定した爻（1〜6）の陰陽を反転させて得られる新しい卦。
 * 互卦: 2・3・4爻目を新しい下卦、3・4・5爻目を新しい上卦とする卦
 *       （初爻・上爻は使わない＝内部に隠れた構造を見る、という古典的な考え方）。
 */

// 八卦名 → 爻の並び（下から上へ）
const TRIGRAM_LINES = {
  乾: [1, 1, 1],
  兌: [1, 1, 0],
  離: [1, 0, 1],
  震: [1, 0, 0],
  巽: [0, 1, 1],
  坎: [0, 1, 0],
  艮: [0, 0, 1],
  坤: [0, 0, 0],
};

// 爻の並び（文字列key）→ 八卦名 の逆引きテーブル
const LINES_TO_TRIGRAM = Object.fromEntries(
  Object.entries(TRIGRAM_LINES).map(([name, lines]) => [lines.join(""), name])
);

function getTrigramLines(name) {
  const lines = TRIGRAM_LINES[name];
  if (!lines) {
    throw new Error(`[bianGuaCalculator] 未知の卦名です: "${name}"`);
  }
  return lines;
}

function linesToTrigramName(lines) {
  const key = lines.join("");
  const name = LINES_TO_TRIGRAM[key];
  if (!name) {
    // 3爻の陽陰の組み合わせは8通りしかないため、通常は起こらない
    throw new Error(`[bianGuaCalculator] 不正な爻の並びです: [${lines.join(",")}]`);
  }
  return name;
}

/**
 * 変卦（へんか）を計算する。
 * 本卦の六爻のうち、指定した1本（changingLine）の陰陽を反転させ、
 * 新しい上卦・下卦を求める。
 *
 * @param {string} upperName    本卦の上卦（八卦名。例: "乾"）
 * @param {string} lowerName    本卦の下卦（八卦名。例: "坤"）
 * @param {number} changingLine 変爻の位置（1〜6。爻1が一番下、爻6が一番上）
 * @returns {{ upperName: string, lowerName: string }} 変卦の上卦・下卦
 *
 * @example
 * // 乾為天（上卦乾・下卦乾）の初爻（爻1）が変爻の場合
 * // 爻1（乾の一番下）が陽→陰に反転 → 新しい下卦は [0,1,1] = 巽
 * computeBianGua("乾", "乾", 1);
 * // => { upperName: "乾", lowerName: "巽" }  （＝ 天風姤）
 *
 * @example
 * // 地天泰（上卦坤・下卦乾）の上爻（爻6、坤の一番上）が変爻の場合
 * // 爻6（坤の一番上）が陰→陽に反転 → 新しい上卦は [0,0,1] = 艮
 * computeBianGua("坤", "乾", 6);
 * // => { upperName: "艮", lowerName: "乾" }  （＝ 山天大畜。易学の教科書で
 * //    「泰の上爻変じて大畜となる」として知られる、標準的な例）
 */
export function computeBianGua(upperName, lowerName, changingLine) {
  if (!Number.isInteger(changingLine) || changingLine < 1 || changingLine > 6) {
    throw new Error(
      `[bianGuaCalculator] changingLineは1〜6の整数である必要があります（受け取った値: ${changingLine}）`
    );
  }

  const lowerLines = getTrigramLines(lowerName);
  const upperLines = getTrigramLines(upperName);
  // 爻1〜爻6（下から上）を1本の配列にする
  const allLines = [...lowerLines, ...upperLines];

  const idx = changingLine - 1;
  allLines[idx] = allLines[idx] === 1 ? 0 : 1;

  const newLowerLines = allLines.slice(0, 3);
  const newUpperLines = allLines.slice(3, 6);

  return {
    upperName: linesToTrigramName(newUpperLines),
    lowerName: linesToTrigramName(newLowerLines),
  };
}

/**
 * 互卦（ごか）を計算する。
 * 本卦の2・3・4爻目を新しい下卦、3・4・5爻目を新しい上卦とする
 * （初爻・上爻は使わない）。
 *
 * @param {string} upperName 本卦の上卦（八卦名）
 * @param {string} lowerName 本卦の下卦（八卦名）
 * @returns {{ upperName: string, lowerName: string }} 互卦の上卦・下卦
 *
 * @example
 * // 地天泰（上卦坤・下卦乾）の互卦
 * // 爻1〜6 = 陽,陽,陽,陰,陰,陰（下から乾3本・上に坤3本）
 * // 新下卦（爻2,3,4） = 陽,陽,陰 = 兌
 * // 新上卦（爻3,4,5） = 陽,陰,陰 = 震
 * computeHuGua("坤", "乾");
 * // => { upperName: "震", lowerName: "兌" }  （＝ 雷沢帰妹。
 * //    「泰の互卦は帰妹」として易学でよく知られる標準的な例）
 */
export function computeHuGua(upperName, lowerName) {
  const lowerLines = getTrigramLines(lowerName);
  const upperLines = getTrigramLines(upperName);
  const allLines = [...lowerLines, ...upperLines]; // 爻1〜爻6（下から上）

  const newLowerLines = [allLines[1], allLines[2], allLines[3]]; // 爻2,3,4
  const newUpperLines = [allLines[2], allLines[3], allLines[4]]; // 爻3,4,5

  return {
    upperName: linesToTrigramName(newUpperLines),
    lowerName: linesToTrigramName(newLowerLines),
  };
}

export default { computeBianGua, computeHuGua };
