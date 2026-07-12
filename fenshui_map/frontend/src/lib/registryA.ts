/**
 * registryA.ts
 * ─────────────────────────────────────────────
 * app/core/registry_a.py の DIRECTIONS / FIVE_ELEMENTS を
 * クライアントサイドへ移植したもの（共有コアのSSOTをTS化）。
 * 静的データなので、サーバーを介さずそのまま使える。
 */

export type DirectionKey =
  | 'north'
  | 'north_east'
  | 'east'
  | 'south_east'
  | 'south'
  | 'south_west'
  | 'west'
  | 'north_west'

export type ElementKey = 'wood' | 'fire' | 'earth' | 'metal' | 'water'

export type DirectionProfile = {
  key: DirectionKey
  labelJa: string
  /** [開始角度, 終了角度)。北(337.5〜22.5)のみ0度をまたぐので特別扱いする */
  degrees: [number, number]
  trigram: string
  element: ElementKey
  season: string
  fengShuiRole: string
}

export type FiveElementProfile = {
  key: ElementKey
  labelJa: string
  generates: ElementKey
  controls: ElementKey
}

export const FIVE_ELEMENTS: Record<ElementKey, FiveElementProfile> = {
  wood: { key: 'wood', labelJa: '木', generates: 'fire', controls: 'earth' },
  fire: { key: 'fire', labelJa: '火', generates: 'earth', controls: 'metal' },
  earth: { key: 'earth', labelJa: '土', generates: 'metal', controls: 'water' },
  metal: { key: 'metal', labelJa: '金', generates: 'water', controls: 'wood' },
  water: { key: 'water', labelJa: '水', generates: 'wood', controls: 'fire' },
}

export const DIRECTIONS: Record<DirectionKey, DirectionProfile> = {
  north: {
    key: 'north', labelJa: '北', degrees: [337.5, 22.5],
    trigram: '坎', element: 'water', season: '冬', fengShuiRole: '玄武',
  },
  north_east: {
    key: 'north_east', labelJa: '北東', degrees: [22.5, 67.5],
    trigram: '艮', element: 'earth', season: '晩冬', fengShuiRole: '鬼門',
  },
  east: {
    key: 'east', labelJa: '東', degrees: [67.5, 112.5],
    trigram: '震', element: 'wood', season: '春', fengShuiRole: '青龍',
  },
  south_east: {
    key: 'south_east', labelJa: '南東', degrees: [112.5, 157.5],
    trigram: '巽', element: 'wood', season: '晩春', fengShuiRole: '風門',
  },
  south: {
    key: 'south', labelJa: '南', degrees: [157.5, 202.5],
    trigram: '離', element: 'fire', season: '夏', fengShuiRole: '朱雀',
  },
  south_west: {
    key: 'south_west', labelJa: '南西', degrees: [202.5, 247.5],
    trigram: '坤', element: 'earth', season: '晩夏', fengShuiRole: '裏鬼門',
  },
  west: {
    key: 'west', labelJa: '西', degrees: [247.5, 292.5],
    trigram: '兌', element: 'metal', season: '秋', fengShuiRole: '白虎',
  },
  north_west: {
    key: 'north_west', labelJa: '北西', degrees: [292.5, 337.5],
    trigram: '乾', element: 'metal', season: '初冬', fengShuiRole: '天門',
  },
}

/**
 * 方位角(0〜360度、真北=0)から、対応する8方位のプロファイルを返す。
 */
export function getDirectionFromHeading(headingDeg: number): DirectionProfile {
  const h = ((headingDeg % 360) + 360) % 360 // 0〜360に正規化
  for (const dir of Object.values(DIRECTIONS)) {
    const [start, end] = dir.degrees
    if (start > end) {
      // 北(337.5〜22.5)のように0度をまたぐケース
      if (h >= start || h < end) return dir
    } else {
      if (h >= start && h < end) return dir
    }
  }
  // 理論上ここには来ない
  return DIRECTIONS.north
}
