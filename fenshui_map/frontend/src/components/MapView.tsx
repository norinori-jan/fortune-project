import { forwardRef, useEffect, useImperativeHandle, useRef } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import type { LatLng } from '../types'

/**
 * MapView.tsx
 * ─────────────────────────────────────────────
 * Google Maps JavaScript API から、国土地理院(GSI)タイルのみで動く
 * Leaflet地図に置き換えたもの。APIキー不要・課金なし。
 *
 * 設計方針:
 *   Props/Handle のインターフェースを特定の地図ライブラリに依存しない形
 *  （LatLng, panTo など）に保っている。将来 Google Maps を使いたく
 *   なった場合も、この同じ Props/Handle を満たす別実装
 *  （例: GoogleMapView.tsx）を作って App.tsx 側の import を
 *   差し替えるだけで済むようにしてある。
 *
 * ベースには「景色」として見やすいGSIの空中写真(seamlessphoto)を使い、
 * 道路・地名が分かるよう標準地図を薄く重ねている。
 */

const GSI_PHOTO_URL = 'https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{z}/{x}/{y}.jpg'
const GSI_STD_URL = 'https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png'
const GSI_HILL_URL = 'https://cyberjapandata.gsi.go.jp/xyz/hillshademap/{z}/{x}/{y}.png'
const GSI_CONTOUR_URL = 'https://cyberjapandata.gsi.go.jp/xyz/contour/{z}/{x}/{y}.png'
const GSI_ATTRIBUTION =
  '<a href="https://maps.gsi.go.jp/development/ichiran.html" target="_blank" rel="noreferrer">地理院タイル</a>'

type Props = {
  initialCenter: LatLng
  gsiVisible: boolean
  gsiOpacity: number
  onCenterChange: (center: LatLng) => void
}

export type MapViewHandle = {
  panTo: (latLng: LatLng) => void
}

const MapView = forwardRef<MapViewHandle, Props>(function MapView(
  { initialCenter, gsiVisible, gsiOpacity, onCenterChange },
  ref,
) {
  const containerRef = useRef<HTMLDivElement | null>(null)
  const mapRef = useRef<L.Map | null>(null)
  const hillLayerRef = useRef<L.TileLayer | null>(null)
  const contourLayerRef = useRef<L.TileLayer | null>(null)

  useImperativeHandle(
    ref,
    () => ({
      panTo(latLng) {
        mapRef.current?.panTo([latLng.lat, latLng.lng])
      },
    }),
    [],
  )

  // 初期化（マウント時に1回だけ）
  useEffect(() => {
    if (!containerRef.current || mapRef.current) return

    const map = L.map(containerRef.current, {
      center: [initialCenter.lat, initialCenter.lng],
      zoom: 17,
      zoomControl: false,
      attributionControl: true,
    })

    // ベースレイヤー: 空中写真（「景色」として見やすくするため標準地図より優先）
    L.tileLayer(GSI_PHOTO_URL, {
      maxZoom: 18,
      attribution: GSI_ATTRIBUTION,
    }).addTo(map)

    // 道路・地名を薄く重ねて位置が分かりやすいようにする
    L.tileLayer(GSI_STD_URL, {
      maxZoom: 18,
      opacity: 0.35,
    }).addTo(map)

    const hill = L.tileLayer(GSI_HILL_URL, { maxZoom: 18, opacity: gsiOpacity })
    const contour = L.tileLayer(GSI_CONTOUR_URL, {
      maxZoom: 18,
      opacity: Math.min(1, gsiOpacity + 0.2),
    })
    hillLayerRef.current = hill
    contourLayerRef.current = contour
    if (gsiVisible) {
      hill.addTo(map)
      contour.addTo(map)
    }

    map.on('moveend', () => {
      const c = map.getCenter()
      onCenterChange({ lat: c.lat, lng: c.lng })
    })

    mapRef.current = map

    return () => {
      map.remove()
      mapRef.current = null
    }
    // 初期化は最初の1回だけでよいので依存配列は空でよい
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // 陰影起伏図・等高線レイヤーの表示切り替え
  useEffect(() => {
    const map = mapRef.current
    const hill = hillLayerRef.current
    const contour = contourLayerRef.current
    if (!map || !hill || !contour) return

    if (gsiVisible) {
      if (!map.hasLayer(hill)) hill.addTo(map)
      if (!map.hasLayer(contour)) contour.addTo(map)
    } else {
      if (map.hasLayer(hill)) map.removeLayer(hill)
      if (map.hasLayer(contour)) map.removeLayer(contour)
    }
  }, [gsiVisible])

  // 不透明度の変更
  useEffect(() => {
    hillLayerRef.current?.setOpacity(gsiOpacity)
    contourLayerRef.current?.setOpacity(Math.min(1, gsiOpacity + 0.2))
  }, [gsiOpacity])

  // FIX: Leafletは初期化時に内部コントロール(.leaflet-top/.leaflet-bottom等)へ
  // 高いz-indexを自前で設定するため、何も指定しないとUIオーバーレイ
  // (コンパス・位置情報パネル・鑑定ボタン等、z-10〜z-50)より地図が
  // 上に乗ってしまうことがある。relative + z-0 を明示して、地図の
  // スタッキングコンテキストをUIより確実に下に固定する。
  return <div ref={containerRef} className="relative z-0 w-full h-full" />
})

export default MapView
