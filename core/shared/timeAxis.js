/**
 * timeAxis.js
 * 干支・九星・梅花心易の時間計算エンジン
 * 既存: fortune-core/src/meihua/utils.js の時間系関数を統合・汎用化
 *
 * 依存: cosmology.js（DIZHI, TIANGAN）
 */

import { DIZHI, TIANGAN, dizhiById } from './cosmology.js';

// ─────────────────────────────────────────────
// 干支計算
// ─────────────────────────────────────────────

/**
 * 年の干支を計算する
 * @param {number} year - 西暦年
 * @returns {{ gan: object, zhi: object, kanshi: string }}
 */
export function yearKanshi(year) {
  const ganIdx  = (year - 4)  % 10;
  const zhiIdx  = (year - 4)  % 12;
  const gan  = TIANGAN[((ganIdx % 10) + 10) % 10];
  const zhi  = DIZHI[((zhiIdx % 12) + 12) % 12];
  return { gan, zhi, kanshi: `${gan.kanji}${zhi.kanji}` };
}

/**
 * 月の干支を計算する（節月基準）
 * @param {number} year  - 西暦年
 * @param {number} month - 1〜12（節入り後）
 * @returns {{ gan: object, zhi: object, kanshi: string }}
 */
export function monthKanshi(year, month) {
  // 月支は固定（寅月=1月節〜）
  // index: 寅=2 が起点
  const zhiIdx = ((month - 1) + 2) % 12;
  const zhi = DIZHI[zhiIdx];

  // 月干は年干から計算
  const yearGanIdx = (year - 4) % 10;
  // 甲・己年は丙寅から始まる
  const monthGanBase = [2, 4, 6, 8, 0, 2, 4, 6, 8, 0][((yearGanIdx % 10) + 10) % 10];
  const ganIdx = (monthGanBase + (month - 1)) % 10;
  const gan = TIANGAN[ganIdx];
  return { gan, zhi, kanshi: `${gan.kanji}${zhi.kanji}` };
}

/**
 * 日の干支を計算する
 * @param {Date} date
 * @returns {{ gan: object, zhi: object, kanshi: string }}
 */
export function dayKanshi(date) {
  // 基準日: 2024-01-01 = 甲子(0,0)
  const base = new Date(2024, 0, 1);
  const diff = Math.floor((date - base) / 86400000);
  const ganIdx = ((diff % 10) + 10) % 10;
  const zhiIdx = ((diff % 12) + 12) % 12;
  const gan = TIANGAN[ganIdx];
  const zhi = DIZHI[zhiIdx];
  return { gan, zhi, kanshi: `${gan.kanji}${zhi.kanji}` };
}

/**
 * 時の干支を計算する
 * @param {number} hour   - 0〜23
 * @param {object} dayGan - 日干オブジェクト（TIANGAN の要素）
 * @returns {{ gan: object, zhi: object, kanshi: string }}
 */
export function hourKanshi(hour, dayGan) {
  // 時支: 子=23,0〜1, 丑=1〜3, ...
  const zhiIdx = Math.floor(((hour + 1) % 24) / 2);
  const zhi = DIZHI[zhiIdx];

  // 時干は日干から計算（五虎遁）
  const timeGanBase = [0, 2, 4, 6, 8, 0, 2, 4, 6, 8][dayGan.index];
  const ganIdx = (timeGanBase + zhiIdx) % 10;
  const gan = TIANGAN[ganIdx];
  return { gan, zhi, kanshi: `${gan.kanji}${zhi.kanji}` };
}

// ─────────────────────────────────────────────
// 九星計算
// ─────────────────────────────────────────────

/** 九星名称 */
export const KYUSEI_NAMES = [
  '', '一白水星', '二黒土星', '三碧木星', '四緑木星',
  '五黄土星', '六白金星', '七赤金星', '八白土星', '九紫火星',
];

/**
 * 年九星を計算する
 * @param {number} year - 西暦年
 * @returns {number} 1〜9
 */
export function yearKyusei(year) {
  return ((11 - (year % 9)) % 9) || 9;
}

/**
 * 月九星を計算する（節月基準）
 * @param {number} year  - 西暦年
 * @param {number} month - 1〜12
 * @returns {number} 1〜9
 */
export function monthKyusei(year, month) {
  const yearK = yearKyusei(year);
  // 年九星ごとの1月（寅月）の月九星基準値
  const base = [0, 8, 5, 2, 8, 5, 2, 8, 5, 2][yearK];
  return ((base - (month - 1) + 9 * 10) % 9) || 9;
}

// ─────────────────────────────────────────────
// 梅花心易 時間数計算
// 既存: fortune-core/src/meihua/utils.js と統合
// ─────────────────────────────────────────────

/**
 * 梅花心易の時間数（時間→数）
 * 子=1, 丑=2, ..., 亥=12
 * @param {number} hour - 0〜23
 * @returns {number} 1〜12
 */
export function meihuaTimeNumber(hour) {
  return Math.floor(((hour + 1) % 24) / 2) + 1;
}

/**
 * 梅花心易 上卦数（年月日時の合計 % 8）
 * @param {Date}   date
 * @param {number} hour
 * @returns {number} 1〜8（八卦番号）
 */
export function meihuaUpperNumber(date, hour) {
  const y = date.getFullYear();
  const m = date.getMonth() + 1;
  const d = date.getDate();
  const h = meihuaTimeNumber(hour);
  const sum = y + m + d + h;
  return ((sum % 8) || 8);
}

/**
 * 梅花心易 下卦数
 * @param {Date}   date
 * @param {number} hour
 * @returns {number} 1〜8
 */
export function meihuaLowerNumber(date, hour) {
  const upper = meihuaUpperNumber(date, hour);
  const h = meihuaTimeNumber(hour);
  return (((upper + h) % 8) || 8);
}

/**
 * 梅花心易 動爻数
 * @param {Date}   date
 * @param {number} hour
 * @returns {number} 1〜6
 */
export function meihuaDongYao(date, hour) {
  const y = date.getFullYear();
  const m = date.getMonth() + 1;
  const d = date.getDate();
  const h = meihuaTimeNumber(hour);
  const sum = y + m + d + h;
  return ((sum % 6) || 6);
}

// ─────────────────────────────────────────────
// 現在の時間コンテキストを一括取得
// ─────────────────────────────────────────────

/**
 * 現在日時から DivinationReading.timeContext を生成する
 * @param {Date} [now=new Date()]
 * @returns {object} timeContext
 */
export function getCurrentTimeContext(now = new Date()) {
  const year  = now.getFullYear();
  const month = now.getMonth() + 1;
  const hour  = now.getHours();

  const yKanshi = yearKanshi(year);
  const mKanshi = monthKanshi(year, month);
  const dKanshi = dayKanshi(now);
  const hKanshi = hourKanshi(hour, dKanshi.gan);

  return {
    junishi:    dKanshi.zhi.kanji,
    kanshi:     yKanshi.kanshi,
    kyusei:     yearKyusei(year),
    monthKyusei: monthKyusei(year, month),
    yearKanshi:  yKanshi.kanshi,
    monthKanshi: mKanshi.kanshi,
    dayKanshi:   dKanshi.kanshi,
    hourKanshi:  hKanshi.kanshi,
    // 六爻用
    yuejian: mKanshi.zhi.id,   // 月建地支ID
    rizhen:  dKanshi.zhi.id,   // 日辰地支ID
  };
}

/**
 * 梅花心易の時間起卦情報を取得する
 * @param {Date} [now=new Date()]
 * @returns {object}
 */
export function getMeihuaTimeInput(now = new Date()) {
  const hour = now.getHours();
  return {
    upperNum:  meihuaUpperNumber(now, hour),
    lowerNum:  meihuaLowerNumber(now, hour),
    dongYao:   meihuaDongYao(now, hour),
    timeCtx:   getCurrentTimeContext(now),
  };
}
