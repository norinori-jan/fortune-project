/**
 * cosmology.js
 * 八卦・五行・十二支・六十四卦 共通データ定義
 * 全アプリはこのファイルからデータを参照する。独自定義禁止。
 *
 * 対応する既存ファイル:
 *   fortune-core/src/meihua/data/hexagram_wuxing.json
 *   fortune-core/src/meihua/data/relations.json
 *   fortune-core/src/meihua/data/time_support.json
 */

// ─────────────────────────────────────────────
// 五行（WuXing）
// ─────────────────────────────────────────────
export const WUXING = Object.freeze({
  WOOD:  { id: 'wood',  kanji: '木', color: 'var(--color-wood)',  index: 0 },
  FIRE:  { id: 'fire',  kanji: '火', color: 'var(--color-fire)',  index: 1 },
  EARTH: { id: 'earth', kanji: '土', color: 'var(--color-earth)', index: 2 },
  METAL: { id: 'metal', kanji: '金', color: 'var(--color-metal)', index: 3 },
  WATER: { id: 'water', kanji: '水', color: 'var(--color-water)', index: 4 },
});

/** 五行相生テーブル: src → 生じる先 */
export const SHENG_TABLE = {
  wood:  'fire',
  fire:  'earth',
  earth: 'metal',
  metal: 'water',
  water: 'wood',
};

/** 五行相克テーブル: src → 克す先 */
export const KE_TABLE = {
  wood:  'earth',
  earth: 'water',
  water: 'fire',
  fire:  'metal',
  metal: 'wood',
};

/**
 * 二つの五行の関係を返す
 * @param {string} src  - 起点五行 ('wood'|'fire'|'earth'|'metal'|'water')
 * @param {string} dst  - 対象五行
 * @returns {'sheng'|'ke'|'he'|'neutral'}
 */
export function wuxingRelation(src, dst) {
  if (src === dst)            return 'he';       // 比和
  if (SHENG_TABLE[src] === dst) return 'sheng';  // 相生
  if (KE_TABLE[src]   === dst) return 'ke';      // 相克
  return 'neutral';
}

// ─────────────────────────────────────────────
// 八卦（BaGua）
// ─────────────────────────────────────────────
export const BAGUA = Object.freeze({
  QIAN: { id: 'qian', kanji: '乾', symbol: '☰', wuxing: 'metal', direction: 'NW', number: 6, nature: '天' },
  DUI:  { id: 'dui',  kanji: '兌', symbol: '☱', wuxing: 'metal', direction: 'W',  number: 7, nature: '沢' },
  LI:   { id: 'li',   kanji: '離', symbol: '☲', wuxing: 'fire',  direction: 'S',  number: 9, nature: '火' },
  ZHEN: { id: 'zhen', kanji: '震', symbol: '☳', wuxing: 'wood',  direction: 'E',  number: 3, nature: '雷' },
  XUN:  { id: 'xun',  kanji: '巽', symbol: '☴', wuxing: 'wood',  direction: 'SE', number: 4, nature: '風' },
  KAN:  { id: 'kan',  kanji: '坎', symbol: '☵', wuxing: 'water', direction: 'N',  number: 1, nature: '水' },
  GEN:  { id: 'gen',  kanji: '艮', symbol: '☶', wuxing: 'earth', direction: 'NE', number: 8, nature: '山' },
  KUN:  { id: 'kun',  kanji: '坤', symbol: '☷', wuxing: 'earth', direction: 'SW', number: 2, nature: '地' },
});

/** 八宮（六爻占の宮）配列順 */
export const BAGUA_GONG_ORDER = ['qian', 'dui', 'li', 'zhen', 'xun', 'kan', 'gen', 'kun'];

// ─────────────────────────────────────────────
// 十二地支（DiZhi）
// ─────────────────────────────────────────────
export const DIZHI = Object.freeze([
  { id: 'zi',   kanji: '子', wuxing: 'water', index: 0,  animal: '鼠' },
  { id: 'chou', kanji: '丑', wuxing: 'earth', index: 1,  animal: '牛' },
  { id: 'yin',  kanji: '寅', wuxing: 'wood',  index: 2,  animal: '虎' },
  { id: 'mao',  kanji: '卯', wuxing: 'wood',  index: 3,  animal: '兎' },
  { id: 'chen', kanji: '辰', wuxing: 'earth', index: 4,  animal: '龍' },
  { id: 'si',   kanji: '巳', wuxing: 'fire',  index: 5,  animal: '蛇' },
  { id: 'wu',   kanji: '午', wuxing: 'fire',  index: 6,  animal: '馬' },
  { id: 'wei',  kanji: '未', wuxing: 'earth', index: 7,  animal: '羊' },
  { id: 'shen', kanji: '申', wuxing: 'metal', index: 8,  animal: '猴' },
  { id: 'you',  kanji: '酉', wuxing: 'metal', index: 9,  animal: '鶏' },
  { id: 'xu',   kanji: '戌', wuxing: 'earth', index: 10, animal: '犬' },
  { id: 'hai',  kanji: '亥', wuxing: 'water', index: 11, animal: '猪' },
]);

/** 地支IDから地支オブジェクトを取得 */
export const dizhiById = Object.fromEntries(DIZHI.map(d => [d.id, d]));

/** 相沖ペア（差が6） */
export const CHONG_PAIRS = [
  ['zi', 'wu'], ['chou', 'wei'], ['yin', 'shen'],
  ['mao', 'you'], ['chen', 'xu'], ['si', 'hai'],
];

/**
 * 二つの地支が相沖かどうか
 * @param {string} a - 地支ID
 * @param {string} b - 地支ID
 * @returns {boolean}
 */
export function isChong(a, b) {
  return CHONG_PAIRS.some(([x, y]) => (x === a && y === b) || (x === b && y === a));
}

// ─────────────────────────────────────────────
// 十干（TianGan）
// ─────────────────────────────────────────────
export const TIANGAN = Object.freeze([
  { id: 'jia',  kanji: '甲', wuxing: 'wood',  yin_yang: 'yang', index: 0 },
  { id: 'yi',   kanji: '乙', wuxing: 'wood',  yin_yang: 'yin',  index: 1 },
  { id: 'bing', kanji: '丙', wuxing: 'fire',  yin_yang: 'yang', index: 2 },
  { id: 'ding', kanji: '丁', wuxing: 'fire',  yin_yang: 'yin',  index: 3 },
  { id: 'wu',   kanji: '戊', wuxing: 'earth', yin_yang: 'yang', index: 4 },
  { id: 'ji',   kanji: '己', wuxing: 'earth', yin_yang: 'yin',  index: 5 },
  { id: 'geng', kanji: '庚', wuxing: 'metal', yin_yang: 'yang', index: 6 },
  { id: 'xin',  kanji: '辛', wuxing: 'metal', yin_yang: 'yin',  index: 7 },
  { id: 'ren',  kanji: '壬', wuxing: 'water', yin_yang: 'yang', index: 8 },
  { id: 'gui',  kanji: '癸', wuxing: 'water', yin_yang: 'yin',  index: 9 },
]);

// ─────────────────────────────────────────────
// 旺衰テーブル（月建ごとの五行強弱）
// 既存: fortune-core/src/meihua/data/time_support.json と対応
// ─────────────────────────────────────────────

/** 月建五行 → 各五行の旺衰 */
export const WANGSHUAI_TABLE = Object.freeze({
  wood:  { wood: 'wang',  fire: 'xiang', water: 'xiu',  metal: 'qi',  earth: 'si'   },
  fire:  { fire: 'wang',  earth: 'xiang', wood: 'xiu',  water: 'qi',  metal: 'si'  },
  earth: { earth: 'wang', metal: 'xiang', fire: 'xiu',  wood: 'qi',   water: 'si'  },
  metal: { metal: 'wang', water: 'xiang', earth: 'xiu', fire: 'qi',   wood: 'si'   },
  water: { water: 'wang', wood: 'xiang',  metal: 'xiu', earth: 'qi',  fire: 'si'   },
});

/**
 * 旺衰スコア（数値化）
 * wang=4, xiang=3, xiu=1, qi=0, si=-1
 */
export const WANGSHUAI_SCORE = { wang: 4, xiang: 3, xiu: 1, qi: 0, si: -1 };

/**
 * 旺衰を取得する
 * @param {string} yaoWuxing   - 爻の五行
 * @param {string} monthWuxing - 月建の五行
 * @returns {'wang'|'xiang'|'xiu'|'qi'|'si'}
 */
export function getWangShuai(yaoWuxing, monthWuxing) {
  return WANGSHUAI_TABLE[monthWuxing]?.[yaoWuxing] ?? 'qi';
}

// ─────────────────────────────────────────────
// 六十四卦 メタデータ（軽量版）
// 詳細は hexagrams.json を参照（SSOTはJSONファイル）
// ─────────────────────────────────────────────

/**
 * 卦番号（1-64）から卦IDを生成するユーティリティ
 * @param {number} num - 1〜64
 * @returns {string} 例: 'hex_01'
 */
export function hexId(num) {
  return `hex_${String(num).padStart(2, '0')}`;
}

/**
 * 上卦・下卦の八卦IDから卦を引く
 * @param {string} upperGua - 上卦ID ('qian'|'dui'|...)
 * @param {string} lowerGua - 下卦ID
 * @returns {number} 卦番号（1-64）
 * ※ King Wen 序卦に準拠した対応表
 */
export const UPPER_LOWER_TO_HEX = Object.freeze({
  'qian-qian': 1,  'qian-dui': 10,  'qian-li': 13,  'qian-zhen': 25,
  'qian-xun':  44, 'qian-kan': 6,   'qian-gen': 33, 'qian-kun':  12,
  'dui-qian':  43, 'dui-dui':  58,  'dui-li':   49, 'dui-zhen':  17,
  'dui-xun':   28, 'dui-kan':  47,  'dui-gen':  31, 'dui-kun':   45,
  'li-qian':   14, 'li-dui':   38,  'li-li':    30, 'li-zhen':   21,
  'li-xun':    50, 'li-kan':   64,  'li-gen':   56, 'li-kun':    35,
  'zhen-qian': 34, 'zhen-dui': 54,  'zhen-li':  55, 'zhen-zhen': 51,
  'zhen-xun':  32, 'zhen-kan': 40,  'zhen-gen': 62, 'zhen-kun':  16,
  'xun-qian':  9,  'xun-dui':  61,  'xun-li':   37, 'xun-zhen':  42,
  'xun-xun':   57, 'xun-kan':  59,  'xun-gen':  53, 'xun-kun':   20,
  'kan-qian':  5,  'kan-dui':  60,  'kan-li':   63, 'kan-zhen':  3,
  'kan-xun':   48, 'kan-kan':  29,  'kan-gen':  39, 'kan-kun':   8,
  'gen-qian':  26, 'gen-dui':  41,  'gen-li':   22, 'gen-zhen':  27,
  'gen-xun':   18, 'gen-kan':  4,   'gen-gen':  52, 'gen-kun':   23,
  'kun-qian':  11, 'kun-dui':  19,  'kun-li':   36, 'kun-zhen':  24,
  'kun-xun':   46, 'kun-kan':  7,   'kun-gen':  15, 'kun-kun':   2,
});

/** 上卦・下卦→卦番号 */
export function getHexNumber(upperGua, lowerGua) {
  return UPPER_LOWER_TO_HEX[`${upperGua}-${lowerGua}`] ?? null;
}

// ─────────────────────────────────────────────
// 六親（LiuQin）
// ─────────────────────────────────────────────
export const LIUQIN = Object.freeze({
  XIONG_DI: { id: 'xiong_di', kanji: '兄弟爻', wuxingRole: 'same',   tarot: 'rivals'  },
  ZI_SUN:   { id: 'zi_sun',   kanji: '子孫爻', wuxingRole: 'output', tarot: 'remedy'  },
  QI_CAI:   { id: 'qi_cai',   kanji: '妻財爻', wuxingRole: 'ke',     tarot: 'wealth'  },
  GUAN_GUI: { id: 'guan_gui', kanji: '官鬼爻', wuxingRole: 'keMe',   tarot: 'obstacle'},
  FU_MU:    { id: 'fu_mu',    kanji: '父母爻', wuxingRole: 'shengMe',tarot: 'support' },
});
