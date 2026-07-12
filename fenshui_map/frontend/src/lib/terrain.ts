import type { TerrainProfile } from '../types'

/**
 * terrain.ts
 * ─────────────────────────────────────────────
 * fenshui_map の app/modules/feng_shui/service.py にあった
 * 国土地理院(GSI)標高APIまわりのロジックを、サーバーを介さず
 * ブラウザから直接叩けるようにクライアントサイドへ移植したもの。
 *
 * GSIの標高APIはAPIキー不要・CC-BY 4.0で、ブラウザからの直接fetchに対応している
 * （地図系のWebデモで広く使われている公開JSON API）。
 * 万一CORSやネットワークで失敗しても、該当地点はnullとして扱い、
 * 呼び出し側（heuristics.ts）が「判定不能」として安全に処理できるようにしてある。
 */

const EARTH_RADIUS_M = 6_378_137
const GSI_ELEVATION_ENDPOINT =
  'https://cyberjapandata2.gsi.go.jp/general/dem/scripts/getelevation.php'

export type Coordinate = { lat: number; lng: number }

/**
 * 中心座標から北方向・東方向にnメートルずらした緯度経度を計算する。
 * service.py の _offset_coordinate() と同じ式。
 */
function offsetCoordinate(origin: Coordinate, northM = 0, eastM = 0): Coordinate {
  const deltaLat = (northM / EARTH_RADIUS_M) * (180 / Math.PI)
  const deltaLng =
    (eastM / (EARTH_RADIUS_M * Math.cos((origin.lat * Math.PI) / 180))) * (180 / Math.PI)
  return { lat: origin.lat + deltaLat, lng: origin.lng + deltaLng }
}

function average(values: Array<number | null>): number | null {
  const valid = values.filter((v): v is number => v !== null)
  if (valid.length === 0) return null
  return valid.reduce((a, b) => a + b, 0) / valid.length
}

/**
 * 単一座標の標高(m)をGSI標高APIから取得する。失敗時はnull。
 */
async function fetchGsiElevationSingle(lat: number, lng: number): Promise<number | null> {
  const url = `${GSI_ELEVATION_ENDPOINT}?lon=${lng}&lat=${lat}&outtype=JSON`
  try {
    const res = await fetch(url)
    if (!res.ok) return null
    const data = (await res.json()) as { elevation?: unknown }
    return typeof data.elevation === 'number' ? data.elevation : null
  } catch {
    // CORSブロック・オフライン・GSI側の一時的な障害などをすべてここで吸収する
    return null
  }
}

/**
 * 中心点＋周囲8点（東西南北の近距離・遠距離）を国土地理院APIでサンプリングし、
 * 東西南北の平均標高差を含む TerrainProfile を返す。
 * service.py の fetch_gsi_terrain_profile() と同じサンプリング設計。
 */
export async function fetchGsiTerrainProfile(
  lat: number,
  lng: number,
  { radiusM = 250, sampleDistanceM = 120 }: { radiusM?: number; sampleDistanceM?: number } = {},
): Promise<TerrainProfile> {
  const center: Coordinate = { lat, lng }
  const points: Record<string, Coordinate> = {
    center,
    north_near: offsetCoordinate(center, sampleDistanceM),
    north_far: offsetCoordinate(center, radiusM),
    south_near: offsetCoordinate(center, -sampleDistanceM),
    south_far: offsetCoordinate(center, -radiusM),
    east_near: offsetCoordinate(center, 0, sampleDistanceM),
    east_far: offsetCoordinate(center, 0, radiusM),
    west_near: offsetCoordinate(center, 0, -sampleDistanceM),
    west_far: offsetCoordinate(center, 0, -radiusM),
  }

  const names = Object.keys(points)
  const elevations = await Promise.all(
    names.map((name) => fetchGsiElevationSingle(points[name].lat, points[name].lng)),
  )
  const byName: Record<string, number | null> = {}
  names.forEach((name, i) => {
    byName[name] = elevations[i]
  })

  return {
    center_elevation_m: byName.center,
    north_avg_elevation_m: average([byName.north_near, byName.north_far]),
    south_avg_elevation_m: average([byName.south_near, byName.south_far]),
    east_avg_elevation_m: average([byName.east_near, byName.east_far]),
    west_avg_elevation_m: average([byName.west_near, byName.west_far]),
    data_source: 'gsi_elevation_api',
  }
}
