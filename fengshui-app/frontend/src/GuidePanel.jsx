import { useEffect, useMemo, useState } from 'react'

function detectMobile() {
  return window.matchMedia('(max-width: 768px)').matches
}

function buildGuideState({ cameraStatus, orientationPermission, directionInfo, houseInfo, captureDataUrl }) {
  if (cameraStatus !== 'granted') {
    return {
      title: 'カメラ未許可',
      message: '今はカメラ許可をしてください。Safariのカメラ権限を許可後、再度開いてください。',
    }
  }

  if (orientationPermission !== 'granted') {
    return {
      title: 'センサー未許可',
      message: '今は「センサー許可」ボタンを押してください。',
    }
  }

  if (!directionInfo || !houseInfo) {
    return {
      title: '方位測定中',
      message: '今は端末をゆっくり水平に動かし、方位が安定するまで待ってください。',
    }
  }

  if (captureDataUrl) {
    return {
      title: '確定済み',
      message: '今は鑑定が確定済みです。必要なら再度「鑑定ボタン」で最新状態を保存してください。',
    }
  }

  return {
    title: '測定完了',
    message: '今は方位測定が完了しています。「鑑定ボタン」で結果を確定してください。',
  }
}

function GuidePanel({ cameraStatus, orientationPermission, directionInfo, houseInfo, captureDataUrl, apiError }) {
  const [isMobile, setIsMobile] = useState(() => detectMobile())
  const [isOpen, setIsOpen] = useState(() => !detectMobile())
  const [touchStartX, setTouchStartX] = useState(null)

  useEffect(() => {
    const onResize = () => {
      const mobile = detectMobile()
      setIsMobile(mobile)
      if (!mobile) {
        setIsOpen(true)
      }
    }

    window.addEventListener('resize', onResize)
    return () => window.removeEventListener('resize', onResize)
  }, [])

  const guide = useMemo(
    () => buildGuideState({ cameraStatus, orientationPermission, directionInfo, houseInfo, captureDataUrl }),
    [cameraStatus, orientationPermission, directionInfo, houseInfo, captureDataUrl],
  )

  const onTouchStart = (event) => {
    setTouchStartX(event.changedTouches?.[0]?.clientX ?? null)
  }

  const onTouchEnd = (event) => {
    if (touchStartX === null) {
      return
    }

    const endX = event.changedTouches?.[0]?.clientX ?? touchStartX
    const delta = endX - touchStartX

    if (isOpen && delta > 40) {
      setIsOpen(false)
    }
    if (!isOpen && delta < -40) {
      setIsOpen(true)
    }
    setTouchStartX(null)
  }

  const panelClassName = `guide-panel ${isOpen ? 'open' : 'closed'} ${isMobile ? 'mobile' : 'desktop'}`

  return (
    <>
      <aside className={panelClassName} onTouchStart={onTouchStart} onTouchEnd={onTouchEnd}>
        <button type="button" className="guide-toggle" onClick={() => setIsOpen((prev) => !prev)} aria-label="使い方ガイドを開閉">
          ❔
        </button>

        <div className="guide-content">
          <h2>使い方ガイド</h2>
          <p className="guide-state">状態: {guide.title}</p>
          <p>{guide.message}</p>

          <ul>
            <li>1) カメラ許可</li>
            <li>2) センサー許可</li>
            <li>3) 方位が安定したら鑑定ボタン</li>
          </ul>

          {apiError && <p className="guide-error">通信エラー検出: {apiError}</p>}
        </div>
      </aside>

      {isMobile && !isOpen && <div className="guide-swipe-edge" onTouchStart={onTouchStart} onTouchEnd={onTouchEnd} />}
    </>
  )
}

export default GuidePanel