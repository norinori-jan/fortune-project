import { useEffect, useState } from 'react'

/**
 * CompassHeading.tsx
 * ─────────────────────────────────────────────
 * 端末の向き（コンパス方位）を画面に表示する。
 * 「景色が動いて、角度が分かればよい」という要望に対応する最小UI。
 *
 * iOS(13以降)のSafariは、deviceorientationイベントを使う前に
 * ユーザー操作（タップ）を起点にした明示的な許可が必要なため、
 * 最初はボタンを表示し、タップされたら許可をリクエストする。
 */

type DeviceOrientationEventiOS = typeof DeviceOrientationEvent & {
  requestPermission?: () => Promise<'granted' | 'denied'>
}

type PermissionState = 'unknown' | 'granted' | 'denied' | 'unsupported'

export default function CompassHeading() {
  const [heading, setHeading] = useState<number | null>(null)
  const [permissionState, setPermissionState] = useState<PermissionState>('unknown')

  useEffect(() => {
    if (permissionState !== 'granted') return

    function handleOrientation(event: DeviceOrientationEvent) {
      // iOS: webkitCompassHeading（真北からの角度、そのまま使える）
      // それ以外: alpha を反転させて近似値として使う
      const iosEvent = event as DeviceOrientationEvent & { webkitCompassHeading?: number }
      if (typeof iosEvent.webkitCompassHeading === 'number') {
        setHeading(iosEvent.webkitCompassHeading)
      } else if (event.alpha !== null) {
        setHeading(360 - event.alpha)
      }
    }

    window.addEventListener('deviceorientation', handleOrientation)
    return () => window.removeEventListener('deviceorientation', handleOrientation)
  }, [permissionState])

  async function requestPermission() {
    const DOE = DeviceOrientationEvent as DeviceOrientationEventiOS
    if (typeof DOE.requestPermission === 'function') {
      // iOS: ユーザー操作(このタップ)を起点に許可をリクエストする必要がある
      try {
        const result = await DOE.requestPermission()
        setPermissionState(result === 'granted' ? 'granted' : 'denied')
      } catch {
        setPermissionState('denied')
      }
    } else if ('DeviceOrientationEvent' in window) {
      // iOS以外（許可リクエスト不要な端末）はそのまま使える
      setPermissionState('granted')
    } else {
      setPermissionState('unsupported')
    }
  }

  if (permissionState === 'unknown') {
    return (
      <button
        onClick={requestPermission}
        className="absolute top-4 left-4 z-40 bg-white/90 rounded-full px-4 py-2 text-sm font-medium text-amber-800 shadow-md"
      >
        🧭 方位を表示
      </button>
    )
  }

  if (permissionState === 'denied' || permissionState === 'unsupported') {
    // 使えない場合は静かに何も出さない（他の操作の邪魔をしない）
    return null
  }

  return (
    <div
      className="absolute top-4 left-4 z-40 bg-white/90 rounded-full w-14 h-14 flex flex-col items-center justify-center shadow-md"
      aria-label="方位"
    >
      <div
        style={{ transform: `rotate(${heading ?? 0}deg)`, transition: 'transform 0.15s linear' }}
        className="text-xl leading-none"
      >
        ⬆️
      </div>
      {heading !== null && (
        <span className="text-[10px] text-gray-500 leading-none mt-0.5">
          {Math.round(heading)}°
        </span>
      )}
    </div>
  )
}
