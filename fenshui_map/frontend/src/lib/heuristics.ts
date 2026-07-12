import type { Heuristics, TerrainProfile } from '../types'

/**
 * heuristics.ts
 * ─────────────────────────────────────────────
 * service.py の evaluate_lantou_heuristics() のうち、地形（標高差）に
 * もとづく判定部分をクライアントサイドへ移植したもの。
 *
 * road_collision_risk（路衝リスク）の判定は、元の実装では
 * Gemini + Google Maps Grounding が周辺の道路を実際に「見て」判定していた。
 * 現段階ではAIを使っていないため、ここは null（判定不能）のまま返す。
 * AIを追加する段階で、この関数はそのまま・またはAIの結果とマージする形で使う想定。
 */
export function evaluateLantouHeuristics(profile: TerrainProfile | null): Heuristics {
  if (!profile || profile.center_elevation_m == null) {
    return {
      shishin_souou: null,
      north_support: null,
      south_open: null,
      east_guard: null,
      west_guard: null,
      road_collision_risk: null,
      confidence: 'low',
    }
  }

  const center = profile.center_elevation_m
  const northDelta = (profile.north_avg_elevation_m ?? center) - center
  const southDelta = (profile.south_avg_elevation_m ?? center) - center
  const eastDelta = (profile.east_avg_elevation_m ?? center) - center
  const westDelta = (profile.west_avg_elevation_m ?? center) - center

  // 閾値は service.py の evaluate_lantou_heuristics() と同じ値に合わせている
  const northSupport = northDelta >= 3
  const southOpen = southDelta <= 1.5
  const eastGuard = eastDelta >= -1
  const westGuard = westDelta >= -1
  const shishinSouou = northSupport && southOpen && eastGuard && westGuard

  return {
    shishin_souou: shishinSouou,
    north_support: northSupport,
    south_open: southOpen,
    east_guard: eastGuard,
    west_guard: westGuard,
    road_collision_risk: null, // AI(Maps Grounding)を追加するまでは判定不能
    confidence: 'medium', // 地形データは取得できているが、AIによる裏付けはまだ無い状態
  }
}

/**
 * AIなし段階の暫定アドバイス文を、判定結果から機械的に組み立てる。
 * 将来 Gemini によるAI鑑定を追加する際は、この関数の呼び出し箇所を
 * 「AIが生成したgrounded_advice」に差し替える想定（ヒューリスティクス自体は流用可）。
 */
export function buildRuleBasedAdvice(heuristics: Heuristics, profile: TerrainProfile | null): string {
  if (!profile || profile.center_elevation_m == null) {
    return '標高データを取得できなかったため、地形にもとづく判定はできませんでした。\n電波状況の良い場所で、もう一度お試しください。'
  }

  const lines: string[] = []
  if (heuristics.shishin_souou) {
    lines.push('地形の高低差から見て、四神相応（北に支え・南が開け・東西に護り）に近い立地です。')
  } else {
    lines.push('地形の高低差から見て、四神相応の条件を完全には満たしていません。')
    if (!heuristics.north_support) lines.push('・北側の標高がやや低く、背後の支えが弱い可能性があります。')
    if (!heuristics.south_open) lines.push('・南側が周囲より高く、開けた印象が弱い可能性があります。')
    if (!heuristics.east_guard) lines.push('・東側の標高が低く、護りが弱い可能性があります。')
    if (!heuristics.west_guard) lines.push('・西側の標高が低く、護りが弱い可能性があります。')
  }
  lines.push('')
  lines.push('※ この結果は国土地理院の標高データのみにもとづく簡易判定です。道路・水回りなどの評価にはAI鑑定（今後追加予定）が必要です。')
  return lines.join('\n')
}
