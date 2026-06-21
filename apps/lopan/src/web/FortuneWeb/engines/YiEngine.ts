// YiEngine.ts
// Fortune Workstation — Web易経エンジン
// 梅花心易: 正確な時支変換 + 事象数を加味した動爻算出

// ============================================================
// § 1. 干支・時支 基本型定義
// ============================================================

/** 十干 (fortune-core の HeavenlyStem に準拠) */
export const HEAVENLY_STEMS = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"] as const;
export type HeavenlyStem = typeof HEAVENLY_STEMS[number];

/** 十二支 */
export const EARTHLY_BRANCHES = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"] as const;
export type EarthlyBranch = typeof EARTHLY_BRANCHES[number];

/** 時支インデックス (0=子, 1=丑, ... 11=亥) */
export type ShizhiIndex = 0|1|2|3|4|5|6|7|8|9|10|11;

/**
 * 時支の開始時刻（24時間制・分）
 * 子: 23:00〜01:00 → 0番目として扱い、前日23時台も子に含める
 */
const SHIZHI_START_MINUTES: readonly number[] = [
  23 * 60,  // 子  23:00〜01:00
   1 * 60,  // 丑  01:00〜03:00
   3 * 60,  // 寅  03:00〜05:00
   5 * 60,  // 卯  05:00〜07:00
   7 * 60,  // 辰  07:00〜09:00
   9 * 60,  // 巳  09:00〜11:00
  11 * 60,  // 午  11:00〜13:00
  13 * 60,  // 未  13:00〜15:00
  15 * 60,  // 申  15:00〜17:00
  17 * 60,  // 酉  17:00〜19:00
  19 * 60,  // 戌  19:00〜21:00
  21 * 60,  // 亥  21:00〜23:00
] as const;

// ============================================================
// § 2. 時支変換ロジック
// ============================================================

/** Date から時支インデックス (0〜11) を算出する */
export function toShizhiIndex(date: Date): ShizhiIndex {
  const h = date.getHours();
  const m = date.getMinutes();
  const totalMinutes = h * 60 + m;

  // 23:00〜23:59 → 子 (0)
  if (totalMinutes >= 23 * 60) return 0;

  // 01:00〜22:59 → 丑〜亥
  for (let i = 10; i >= 1; i--) {
    if (totalMinutes >= SHIZHI_START_MINUTES[i]) return i as ShizhiIndex;
  }

  // 00:00〜00:59 → 子 (0)  ← 深夜0時台も「子」
  return 0;
}

/** 時支インデックス → 十二支文字 */
export function shizhiName(idx: ShizhiIndex): EarthlyBranch {
  return EARTHLY_BRANCHES[idx];
}

/** 時支インデックス → 数値（梅花心易の時数: 子=1, 丑=2 ... 亥=12） */
export function shizhiNumber(idx: ShizhiIndex): number {
  return idx + 1; // 0-indexed → 1〜12
}

/** Date から時支の全情報をまとめて返すユーティリティ */
export interface ShizhiResult {
  index: ShizhiIndex;   // 0〜11
  name: EarthlyBranch;  // "子"〜"亥"
  number: number;        // 1〜12
  rangeLabel: string;   // "23:00〜01:00"
}

export function getShizhi(date: Date): ShizhiResult {
  const idx = toShizhiIndex(date);
  const startH = Math.floor(SHIZHI_START_MINUTES[idx] / 60) % 24;
  const endH   = (startH + 2) % 24;
  return {
    index: idx,
    name: shizhiName(idx),
    number: shizhiNumber(idx),
    rangeLabel: `${String(startH).padStart(2,"0")}:00〜${String(endH).padStart(2,"0")}:00`,
  };
}

// ============================================================
// § 3. 易数（数値）ユーティリティ
// ============================================================

/** 任意の正整数を 1〜8 に折りたたむ（梅花心易の余数変換） */
export function toTrigramNumber(n: number): 1|2|3|4|5|6|7|8 {
  if (n <= 0) throw new Error(`Invalid input: ${n}`);
  const r = n % 8;
  return (r === 0 ? 8 : r) as 1|2|3|4|5|6|7|8;
}

/** 任意の正整数を 1〜6 に折りたたむ（動爻番号算出用） */
export function toLineNumber(n: number): 1|2|3|4|5|6 {
  if (n <= 0) throw new Error(`Invalid input: ${n}`);
  const r = n % 6;
  return (r === 0 ? 6 : r) as 1|2|3|4|5|6;
}

// ============================================================
// § 4. 八卦定義（fortune-core 準拠）
// ============================================================

export type TrigramNumber = 1|2|3|4|5|6|7|8;

export interface Trigram {
  number: TrigramNumber;
  name: string;       // "乾"
  symbol: string;     // "☰"
  nature: string;     // "天"
  element: string;    // "金"
  lines: [0|1, 0|1, 0|1]; // 下→上、1=陽、0=陰
}

export const TRIGRAMS: Record<TrigramNumber, Trigram> = {
  1: { number:1, name:"乾", symbol:"☰", nature:"天", element:"金", lines:[1,1,1] },
  2: { number:2, name:"兌", symbol:"☱", nature:"沢", element:"金", lines:[0,1,1] },
  3: { number:3, name:"離", symbol:"☲", nature:"火", element:"火", lines:[1,0,1] },
  4: { number:4, name:"震", symbol:"☳", nature:"雷", element:"木", lines:[0,0,1] },
  5: { number:5, name:"巽", symbol:"☴", nature:"風", element:"木", lines:[1,1,0] },
  6: { number:6, name:"坎", symbol:"☵", nature:"水", element:"水", lines:[0,1,0] },
  7: { number:7, name:"艮", symbol:"☶", nature:"山", element:"土", lines:[1,0,0] },
  8: { number:8, name:"坤", symbol:"☷", nature:"地", element:"土", lines:[0,0,0] },
};

// ============================================================
// § 5. 梅花心易の卦算出ロジック
// ============================================================

/**
 * 梅花心易における「数」の取り方
 *
 * 年月日時の各数値 + 事象数（観梅数など）を組み合わせて上下卦と動爻を決定する。
 * 本実装は「時間起卦法」に対応。
 */

export interface HexagramInput {
  date: Date;
  /** 事象数（観察した事柄の数。例：梅の花びら落下数、音の回数等） */
  eventNumber?: number;
  /** 上数を手動指定する場合（省略時は年+月+日で自動算出） */
  upperNumberOverride?: number;
  /** 下数を手動指定する場合（省略時は時支数で自動算出） */
  lowerNumberOverride?: number;
}

export interface HexagramResult {
  upperTrigram: Trigram;
  lowerTrigram: Trigram;
  movingLine: 1|2|3|4|5|6;
  hexagramNumber: number;       // 1〜64（将来的に六十四卦マッピング用）
  calculationLog: CalculationLog;
}

export interface CalculationLog {
  year: number;
  month: number;
  day: number;
  shizhi: ShizhiResult;
  eventNumber: number;
  upperSum: number;
  lowerSum: number;
  movingSum: number;
  upperTrigramNumber: TrigramNumber;
  lowerTrigramNumber: TrigramNumber;
}

/**
 * 梅花心易・時間起卦
 *
 * 計算式:
 *   上卦 = (年数 + 月数 + 日数) % 8  ← 0→8
 *   下卦 = (上卦数 + 時支数) % 8
 *   動爻 = (上卦数 + 時支数 + 事象数) % 6 ← 0→6
 *
 * 参考: 邵康節『梅花易数』の「時間起卦法」に準拠
 */
export function calculateHexagram(input: HexagramInput): HexagramResult {
  const { date, eventNumber = 0 } = input;

  const year  = date.getFullYear();
  const month = date.getMonth() + 1;  // 0-indexed → 1〜12
  const day   = date.getDate();
  const shizhi = getShizhi(date);

  // 年数: 下2桁の各桁の和（例: 2024 → 2+0+2+4=8）
  // ※ fortune-core の YearNumber 定義: 西暦年を1桁ずつ加算
  const yearDigitSum = String(year)
    .split("")
    .reduce((acc, d) => acc + parseInt(d, 10), 0);

  // 上卦の元数
  const upperRaw = input.upperNumberOverride ?? (yearDigitSum + month + day);
  // 下卦の元数
  const lowerRaw = input.lowerNumberOverride ?? (toTrigramNumber(upperRaw) + shizhi.number);
  // 動爻の元数（上卦数 + 時支数 + 事象数）
  const movingRaw = toTrigramNumber(upperRaw) + shizhi.number + eventNumber;

  const upperTrigramNumber = toTrigramNumber(upperRaw);
  const lowerTrigramNumber = toTrigramNumber(lowerRaw);
  const movingLine         = toLineNumber(movingRaw);

  // 六十四卦番号（上卦×8 + 下卦 のシンプルマッピング、実際の卦序は別途マップが必要）
  const hexagramNumber = (upperTrigramNumber - 1) * 8 + lowerTrigramNumber;

  const log: CalculationLog = {
    year, month, day,
    shizhi,
    eventNumber,
    upperSum: upperRaw,
    lowerSum: lowerRaw,
    movingSum: movingRaw,
    upperTrigramNumber,
    lowerTrigramNumber,
  };

  return {
    upperTrigram: TRIGRAMS[upperTrigramNumber],
    lowerTrigram: TRIGRAMS[lowerTrigramNumber],
    movingLine,
    hexagramNumber,
    calculationLog: log,
  };
}

// ============================================================
// § 6. 計算過程の人間可読テキスト生成（デバッグ・UI表示用）
// ============================================================

export function formatCalculationLog(r: HexagramResult): string {
  const l = r.calculationLog;
  const lines = [
    `【梅花心易 起卦ログ】`,
    `起卦日時 : ${l.year}年${l.month}月${l.day}日  ${l.shizhi.name}時（${l.shizhi.rangeLabel}）`,
    `時支数   : ${l.shizhi.number}（${l.shizhi.name}）`,
    `事象数   : ${l.eventNumber}`,
    `──────────────────────`,
    `上卦算出 : ${l.year} → 各桁和 + ${l.month}月 + ${l.day}日 = ${l.upperSum} → ${l.upperTrigramNumber}（÷8の余り）`,
    `上卦     : ${TRIGRAMS[l.upperTrigramNumber].symbol} ${TRIGRAMS[l.upperTrigramNumber].name}（第${l.upperTrigramNumber}卦）`,
    `下卦算出 : ${l.upperTrigramNumber}（上卦数）+ ${l.shizhi.number}（時支数）= ${l.lowerSum} → ${l.lowerTrigramNumber}`,
    `下卦     : ${TRIGRAMS[l.lowerTrigramNumber].symbol} ${TRIGRAMS[l.lowerTrigramNumber].name}（第${l.lowerTrigramNumber}卦）`,
    `動爻算出 : ${l.upperTrigramNumber} + ${l.shizhi.number} + ${l.eventNumber}（事象数）= ${l.movingSum} → 第${r.movingLine}爻`,
    `──────────────────────`,
    `本卦     : ${TRIGRAMS[l.upperTrigramNumber].symbol}${TRIGRAMS[l.lowerTrigramNumber].symbol}  上${TRIGRAMS[l.upperTrigramNumber].name} / 下${TRIGRAMS[l.lowerTrigramNumber].name}`,
    `動爻     : 第${r.movingLine}爻動`,
  ];
  return lines.join("\n");
}

// ============================================================
// § 7. 使用例
// ============================================================

/*
const result = calculateHexagram({
  date: new Date("2025-06-15T14:30:00"),
  eventNumber: 3,  // 例: 鳥が3回鳴いた
});

console.log(formatCalculationLog(result));

export const HEXAGRAM_NAMES: { [key: number]: string } = {
    1: "乾為天", 2: "坤為地", 3: "水雷屯", 4: "山水蒙",
    // ... 中略（全64卦分、代表的なものをまず定義）
};

// 補助関数：番号から名前を返す
export function getHexagramName(num: number): string {
    return HEXAGRAM_NAMES[num] || `第${num}卦`;
}
// 出力例:
// 【梅花心易 起卦ログ】
// 起卦日時 : 2025年6月15日  未時（13:00〜15:00）
// 時支数   : 8（未）
// 事象数   : 3
// ──────────────────────
// 上卦算出 : 2025 → 各桁和 + 6月 + 15日 = 30 → 6（÷8の余り）
// 上卦     : ☵ 坎（第6卦）
// 下卦算出 : 6（上卦数）+ 8（時支数）= 14 → 6
// 下卦     : ☵ 坎（第6卦）
// 動爻算出 : 6 + 8 + 3（事象数）= 17 → 第5爻
// ──────────────────────
// 本卦     : ☵☵  上坎 / 下坎
// 動爻     : 第5爻動
*/