import { useEffect, useMemo, useRef, useState } from 'react'
import './App.css'
import { saveToSpreadsheet, getMapUrl, getShiShuDivination, generateNatalChart } from './api'
import CameraView from './CameraView'
import { layers, analyzeAllLayers, MOUNTAIN_LABELS, LOPAN_MASTER_DATA } from './lopanDatabase'

// ─────────────────────────────────────────────
// 六十四卦データ（易占モード用）
// ─────────────────────────────────────────────
const HEXAGRAMS = [
  {
    number: '䷀',
    name: '乾為天',
    reading: '大吉',
    color: '#FFD700',
    keyword: '剛健・創始・天の徳',
    message:
      '天の気が満ち満ちています。あなたの志は正しく、力強く前進する時。迷わず己の道を歩み、大きな成果が期待できます。ただし、高みに昇りすぎると転落の危険もあり。謙虚さを忘れずに。',
    advice: '積極的に行動せよ。好機は今。',
  },
  {
    number: '䷁',
    name: '坤為地',
    reading: '吉',
    color: '#8BC34A',
    keyword: '従順・包容・大地の徳',
    message:
      '大地のように静かに、ゆっくりと育む時です。焦らず、人の意見に耳を傾け、地道な努力を積み重ねることで、やがて大きな実りをもたらします。今は先頭に立つより、支える役割が吉。',
    advice: '焦らず着実に。土台を固めよ。',
  },
  {
    number: '䷂',
    name: '水雷屯',
    reading: '小吉',
    color: '#64B5F6',
    keyword: '創業・困難・芽吹き',
    message:
      '物事の始まりには必ず苦労が伴います。今は困難な時期ですが、これは成長の糧。焦って動けば失敗しますが、しっかりと根を張り忍耐すれば、やがて大きく芽吹きます。信頼できる人の助けを借りよ。',
    advice: '急がず、信頼できる人に相談を。',
  },
  {
    number: '䷉',
    name: '天澤履',
    reading: '中吉',
    color: '#CE93D8',
    keyword: '礼・慎重・危険の中の礼節',
    message:
      '虎の尾を踏むような状況ですが、礼節と誠実さをもって進めば、危険を免れます。身の程をわきまえ、正しい振る舞いを心がけることが最大の護符となります。軽率な言動は慎んでください。',
    advice: '礼儀を正し、誠実に行動せよ。',
  },
  {
    number: '䷋',
    name: '天地否',
    reading: '凶',
    color: '#EF5350',
    keyword: '閉塞・停滞・陰陽不交',
    message:
      '天と地が交わらず、物事が行き詰まる時。今は無理に前進せず、内に籠もって力を蓄える時期です。現状維持を心がけ、次の好機をじっくり待ちましょう。この停滞は必ず終わります。',
    advice: '待機の時。内省し、力を蓄えよ。',
  },
  {
    number: '䷡',
    name: '雷天大壮',
    reading: '吉',
    color: '#FF9800',
    keyword: '壮大・勢い・過信に注意',
    message:
      '雷鳴のような勢いと活力に満ちています。強い力がありますが、その力を正しい目的に使うことが肝要です。過信や強引さは禍を招きます。正義の道を歩めば、大きな前進が期待できます。',
    advice: '力を正しく使え。驕りを戒めよ。',
  },
  {
    number: '䷿',
    name: '火水未済',
    reading: '小凶',
    color: '#FF7043',
    keyword: '未完成・もう少し・最後の踏ん張り',
    message:
      'ゴールはすぐそこですが、まだ完成していません。最後の一歩を誤ると全てが水の泡。今こそ慎重に、焦らず確実に仕上げる時です。惜しいところまで来ているだけに、気を引き締めてください。',
    advice: '最後まで油断せず、丁寧に締めくくれ。',
  },
]

// ─────────────────────────────────────────────
// ユーティリティ
// ─────────────────────────────────────────────
const polarToCartesian = (cx, cy, radius, angle) => {
  const rad = (angle - 90) * (Math.PI / 180)
  return { x: cx + Math.cos(rad) * radius, y: cy + Math.sin(rad) * radius }
}

const describeArcSegment = (cx, cy, innerR, outerR, startAngle, endAngle) => {
  const startOuter = polarToCartesian(cx, cy, outerR, endAngle)
  const endOuter   = polarToCartesian(cx, cy, outerR, startAngle)
  const endInner   = polarToCartesian(cx, cy, innerR, startAngle)
  const startInner = polarToCartesian(cx, cy, innerR, endAngle)
  const largeArcFlag = endAngle - startAngle <= 180 ? 0 : 1
  return [
    `M ${startOuter.x} ${startOuter.y}`,
    `A ${outerR} ${outerR} 0 ${largeArcFlag} 0 ${endOuter.x} ${endOuter.y}`,
    `L ${endInner.x} ${endInner.y}`,
    `A ${innerR} ${innerR} 0 ${largeArcFlag} 1 ${startInner.x} ${startInner.y}`,
    'Z',
  ].join(' ')
}

// ─────────────────────────────────────────────
// App
// ─────────────────────────────────────────────
function App() {
  const videoRef = useRef(null)
  const [heading, setHeading]                   = useState(0)
  const [laserPos, setLaserPos]                 = useState(window.innerWidth / 2)
  const [viewMode, setViewMode]                 = useState('camera')
  const [mapUrl, setMapUrl]                     = useState('')
  const [note, setNote]                         = useState('')
  const [isPanelOpen, setIsPanelOpen]           = useState(false)
  const [saveStatus, setSaveStatus]             = useState('idle')
  const [selectedCameraId, setSelectedCameraId] = useState('')
  const [compassStatus, setCompassStatus]       = useState('未有効')
  const [activeLayer, setActiveLayer]           = useState('L1')
  const headingQueueRef = useRef([])
  const rafRef          = useRef(null)

  // 鑑定モード共通
  const [divinationMode, setDivinationMode] = useState('風水鑑定')
  const [userQuery, setUserQuery]           = useState('今年の運勢は？')

  // 四柱推命 state
  const [shiShuYear,   setShiShuYear]   = useState('')
  const [shiShuMonth,  setShiShuMonth]  = useState('')
  const [shiShuDay,    setShiShuDay]    = useState('')
  const [shiShuHour,   setShiShuHour]   = useState('')
  const [shiShuGender, setShiShuGender] = useState('不明')
  const [aiResult,     setAiResult]     = useState(null)
  const [aiLoading,    setAiLoading]    = useState(false)

  // 易占 state
  const [divinationResult, setDivinationResult] = useState(null)

  // 角度計算
  const combinedAngle = useMemo(() => {
    const rel = (laserPos - window.innerWidth / 2) / window.innerWidth
    return (heading + rel * 90 + 360) % 360
  }, [heading, laserPos])

  const analyzed = useMemo(() => analyzeAllLayers(combinedAngle), [combinedAngle])

  const getLayerText = (layer) => analyzed[layer] || analyzed.L1

  // デバイス方位センサー
  useEffect(() => {
    const handleOrientation = (e) => {
      let raw = null
      if (e.webkitCompassHeading != null) {
        raw = e.webkitCompassHeading
      } else if (e.alpha != null) {
        raw = (360 - e.alpha) % 360
      }
      if (raw != null && !isNaN(raw)) {
        headingQueueRef.current.push(raw)
        if (headingQueueRef.current.length > 5) headingQueueRef.current.shift()
      }
    }
    const tick = () => {
      const values = headingQueueRef.current
      if (values.length > 0) {
        const average = values.reduce((sum, v) => sum + v, 0) / values.length
        setHeading(average)
      }
      rafRef.current = requestAnimationFrame(tick)
    }
    window.addEventListener('deviceorientation', handleOrientation, true)
    rafRef.current = requestAnimationFrame(tick)
    return () => {
      window.removeEventListener('deviceorientation', handleOrientation, true)
      if (rafRef.current) cancelAnimationFrame(rafRef.current)
    }
  }, [])

  // コンパス権限取得
  const handleEnableCompass = async () => {
    if (
      typeof DeviceOrientationEvent !== 'undefined' &&
      typeof DeviceOrientationEvent.requestPermission === 'function'
    ) {
      try {
        const permission = await DeviceOrientationEvent.requestPermission()
        setCompassStatus(permission === 'granted' ? '回転センサー有効' : '権限が拒否されました')
      } catch {
        setCompassStatus('権限取得に失敗')
      }
    } else {
      setCompassStatus('センサー準備完了')
    }
  }

  // スプレッドシート保存
  const handleSave = async () => {
    setSaveStatus('loading')
    let elevation = '取得失敗'
    try {
      const pos = await new Promise((res, rej) =>
        navigator.geolocation.getCurrentPosition(res, rej, { enableHighAccuracy: true })
      )
      const { latitude, longitude } = pos.coords
      const elevRes  = await fetch(
        `https://cyberjapandata2.gsi.go.jp/visno/cgi-bin/query/getelevation.php?lon=${longitude}&lat=${latitude}&outtype=JSON`
      )
      const elevData = await elevRes.json()
      elevation = elevData.elevation !== '-----' ? `${elevData.elevation}m` : '計測不能'
      const success = await saveToSpreadsheet({
        angle: combinedAngle.toFixed(1),
        L1: analyzed.L1,   L2: analyzed.L2,   L3: analyzed.L3,
        L4: analyzed.L4,   L5: analyzed.L5,   L6: analyzed.L6,
        L7: analyzed.L7,   L8: analyzed.L8,   L9: analyzed.L9,
        L10: analyzed.L10, L11: analyzed.L11, L12: analyzed.L12,
        L13: analyzed.L13,
        L14_八卦: analyzed.L14,
        L15_卦名: analyzed.L15,
        L16_九星方位: analyzed.L16,
        L17_外卦: analyzed.L17,
        L19_干支: analyzed.L19,
        L20_属性九星: analyzed.L20,
        isImportant: analyzed.isImportant ? '重要' : '通常',
        elevation,
        note,
      })
      if (success) {
        setSaveStatus('success')
        setTimeout(() => { setSaveStatus('idle'); setNote('') }, 2000)
      }
    } catch {
      alert('位置情報の取得に失敗しました。iPhoneの設定でブラウザの位置情報を許可してください。')
      setSaveStatus('idle')
    }
  }

  // 四柱推命 AI 鑑定
  const handleExecuteDivination = async () => {
    if (divinationMode === '四柱推命' && (!shiShuYear || !shiShuMonth || !shiShuDay)) {
      alert('生年月日を入力してください')
      return
    }
    setAiLoading(true)
    try {
      const natalChart = generateNatalChart(
        shiShuYear, shiShuMonth, shiShuDay, shiShuHour || null, shiShuGender
      )
      const result = await getShiShuDivination(natalChart, userQuery)
      setAiResult(result)
    } catch (err) {
      setAiResult({ status: 'error', divination: `エラーが発生しました: ${err.message}` })
    } finally {
      setAiLoading(false)
    }
  }

  // 易占 ランダム抽選
  const handleYiDivination = () => {
    setDivinationResult(HEXAGRAMS[Math.floor(Math.random() * HEXAGRAMS.length)])
  }

  // SVG 定数
  const compassSize     = 440
  const center          = compassSize / 2
  const activeSlotStart = Math.floor(analyzed.normalized / 15) * 15 - 90
  const activeSlotEnd   = activeSlotStart + 15

  return (
    <div className="app-root">

      {/* カメラ / 地図レイヤー */}
      <div className="camera-layer">
        {viewMode === 'camera' ? (
          <CameraView videoRef={videoRef} deviceId={selectedCameraId} />
        ) : (
          <iframe src={mapUrl} style={{ width: '100%', height: '100%', border: 'none' }} />
        )}
      </div>

      {/* 羅盤 SVG */}
      <div
        className="compass-graphic"
        style={{ transform: `translate(-50%, -50%) rotate(${-heading}deg)` }}
      >
        <svg width={compassSize} height={compassSize} className="compass-svg">
          <defs>
            <radialGradient id="compassGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%"   stopColor="rgba(212,175,55,0.45)" />
              <stop offset="100%" stopColor="rgba(212,175,55,0.04)" />
            </radialGradient>
          </defs>

          <circle
            cx={center} cy={center} r={center - 8}
            fill="none" stroke="rgba(212,175,55,0.7)" strokeWidth="2"
          />
          <path
            d={describeArcSegment(center, center, 190, 230, activeSlotStart, activeSlotEnd)}
            fill={analyzed.isImportant ? 'rgba(255,100,100,0.15)' : 'rgba(255,255,255,0.08)'}
          />

          {/* 5度刻みティック */}
          {Array.from({ length: 72 }).map((_, i) => {
            const angle = i * 5
            const outer = polarToCartesian(center, center, 230, angle)
            const inner = polarToCartesian(center, center, 220, angle)
            return (
              <line
                key={`tick360-${i}`}
                x1={outer.x} y1={outer.y}
                x2={inner.x} y2={inner.y}
                stroke="rgba(212,175,55,0.7)"
                strokeWidth={angle % 15 === 0 ? 2 : 1}
              />
            )
          })}

          {/* 二十四山ラベル */}
          {Array.from({ length: 24 }).map((_, i) => {
            const angle    = i * 15
            const labelPos = polarToCartesian(center, center, 205, angle)
            return (
              <g key={`slot-${i}`}>
                <line
                  x1={polarToCartesian(center, center, 218, angle).x}
                  y1={polarToCartesian(center, center, 218, angle).y}
                  x2={polarToCartesian(center, center, 230, angle).x}
                  y2={polarToCartesian(center, center, 230, angle).y}
                  stroke="#d4af37" strokeWidth="2"
                />
                <text
                  x={labelPos.x} y={labelPos.y + 6}
                  fill="#ffd46b" fontSize="12" fontWeight="700" textAnchor="middle"
                >
                  {MOUNTAIN_LABELS[i]}
                </text>
              </g>
            )
          })}

          {/* L7 レイヤー */}
          {Array.from({ length: 8 }).flatMap((_, guaIdx) => {
            const gua = LOPAN_MASTER_DATA && LOPAN_MASTER_DATA[guaIdx]
            if (!gua || !gua.slots) return []
            return gua.slots.flatMap((slot, slotIdx) => {
              if (!slot || !slot.l7) return []
              const baseAngle = guaIdx * 45 + slotIdx * 15
              return slot.l7.map((label, idx) => {
                const angle    = baseAngle + idx * 5
                const start    = polarToCartesian(center, center, 180, angle)
                const end      = polarToCartesian(center, center, 190, angle)
                const labelPos = polarToCartesian(center, center, 172, angle)
                return (
                  <g key={`l7-${guaIdx}-${slotIdx}-${idx}`}>
                    <line
                      x1={start.x} y1={start.y}
                      x2={end.x}   y2={end.y}
                      stroke="rgba(255,255,255,0.65)" strokeWidth="1"
                    />
                    <text
                      x={labelPos.x} y={labelPos.y + 4}
                      fill={slot.is_important ? '#ff6b6b' : '#fff'}
                      fontSize="8" textAnchor="middle"
                    >
                      {label}
                    </text>
                  </g>
                )
              })
            })
          })}

          {/* L8 レイヤー */}
          {Array.from({ length: 8 }).flatMap((_, guaIdx) => {
            const gua = LOPAN_MASTER_DATA && LOPAN_MASTER_DATA[guaIdx]
            if (!gua || !gua.slots) return []
            return gua.slots.flatMap((slot, slotIdx) => {
              if (!slot || !slot.l8) return []
              const baseAngle = guaIdx * 45 + slotIdx * 15
              return slot.l8.map((label, idx) => {
                const angle    = baseAngle + idx * 3
                const start    = polarToCartesian(center, center, 155, angle)
                const end      = polarToCartesian(center, center, 160, angle)
                const labelPos = polarToCartesian(center, center, 145, angle)
                return (
                  <g key={`l8-${guaIdx}-${slotIdx}-${idx}`}>
                    <line
                      x1={start.x} y1={start.y}
                      x2={end.x}   y2={end.y}
                      stroke="rgba(255,255,255,0.55)" strokeWidth="1"
                    />
                    {label !== '空白' && (
                      <text
                        x={labelPos.x} y={labelPos.y + 3}
                        fill="#c8d6ff" fontSize="7" textAnchor="middle"
                      >
                        {label}
                      </text>
                    )}
                  </g>
                )
              })
            })
          })}

          {/* 中央表示 */}
          <circle
            cx={center} cy={center} r={110}
            fill="rgba(0,0,0,0.65)" stroke="rgba(212,175,55,0.8)" strokeWidth="2"
          />
          <text
            x={center} y={center - 14}
            fill={analyzed.isImportant ? '#ff6b6b' : '#fff'}
            fontSize="46" fontWeight="900" textAnchor="middle" dominantBaseline="middle"
          >
            {getLayerText(activeLayer)}
          </text>
          <text
            x={center} y={center + 24}
            fill="#fff" fontSize="16" textAnchor="middle" dominantBaseline="middle"
          >
            {analyzed.L2_二十四山}
          </text>
        </svg>
      </div>

      {/* 中央オーバーレイ */}
      <div className="center-overlay">
        <p className="overlay-mountain">{getLayerText(activeLayer)}</p>
        <p className="overlay-degree">{analyzed.angle}</p>
      </div>

      {/* 上部コントロール */}
      <div className="control-top">
        <button className="primary-btn" onClick={() => setViewMode('camera')}>📸</button>
        <button
          className="primary-btn"
          onClick={async () => { setMapUrl(await getMapUrl('gsi')); setViewMode('gsi') }}
        >🗾</button>
        <button className="primary-btn" onClick={() => setIsPanelOpen(true)}>⚙️</button>
      </div>

      {/* サイドパネル */}
      <div className={`guide-panel ${isPanelOpen ? 'open' : ''}`}>
        <button className="guide-toggle" onClick={() => setIsPanelOpen(!isPanelOpen)}>
          {isPanelOpen ? '▶' : '◀'}
        </button>

        <div className="guide-content">
          <h2 className="guide-state">鑑定メニュー</h2>
          <button className="panel-btn activate-btn" onClick={handleEnableCompass}>
            羅盤をアクティブにする
          </button>
          <p className="small-note">センサー状態: {compassStatus}</p>

          {/* 鑑定モード切り替えタブ */}
          <div style={{
            display: 'flex', gap: '8px',
            marginBottom: '15px',
            borderBottom: '1px solid #555', paddingBottom: '10px',
          }}>
            {['風水鑑定', '四柱推命', '易占'].map(mode => (
              <button
                key={mode}
                onClick={() => setDivinationMode(mode)}
                style={{
                  flex: 1, padding: '8px',
                  background: divinationMode === mode ? '#d4af37' : '#333',
                  color:      divinationMode === mode ? '#000'    : '#fff',
                  border: '1px solid #555', borderRadius: '4px',
                  fontSize: '11px', fontWeight: 'bold',
                  cursor: 'pointer', transition: 'all 0.3s',
                }}
              >
                {mode}
              </button>
            ))}
          </div>

          {/* ════ 四柱推命フォーム ════ */}
          {divinationMode === '四柱推命' && (
            <div style={{
              marginBottom: '15px', padding: '10px',
              background: '#2a2a2a', borderRadius: '5px', border: '1px solid #555',
            }}>
              <h3 style={{ fontSize: '12px', marginBottom: '8px', color: '#d4af37' }}>
                生年月日入力
              </h3>

              <div style={{ marginBottom: '8px' }}>
                <label style={{ fontSize: '10px', opacity: 0.7, display: 'block', marginBottom: '4px' }}>
                  生年（西暦）
                </label>
                <input
                  type="number" min="1900" max={new Date().getFullYear()}
                  value={shiShuYear} onChange={(e) => setShiShuYear(e.target.value)}
                  placeholder="1990"
                  style={{ width: '100%', padding: '6px', background: '#333', border: '1px solid #555', borderRadius: '4px', color: '#fff', fontSize: '11px' }}
                />
              </div>

              <div style={{ display: 'flex', gap: '8px', marginBottom: '8px' }}>
                <div style={{ flex: 1 }}>
                  <label style={{ fontSize: '10px', opacity: 0.7, display: 'block', marginBottom: '4px' }}>月</label>
                  <input
                    type="number" min="1" max="12"
                    value={shiShuMonth} onChange={(e) => setShiShuMonth(e.target.value)}
                    placeholder="1-12"
                    style={{ width: '100%', padding: '6px', background: '#333', border: '1px solid #555', borderRadius: '4px', color: '#fff', fontSize: '11px' }}
                  />
                </div>
                <div style={{ flex: 1 }}>
                  <label style={{ fontSize: '10px', opacity: 0.7, display: 'block', marginBottom: '4px' }}>日</label>
                  <input
                    type="number" min="1" max="31"
                    value={shiShuDay} onChange={(e) => setShiShuDay(e.target.value)}
                    placeholder="1-31"
                    style={{ width: '100%', padding: '6px', background: '#333', border: '1px solid #555', borderRadius: '4px', color: '#fff', fontSize: '11px' }}
                  />
                </div>
              </div>

              <div style={{ marginBottom: '8px' }}>
                <label style={{ fontSize: '10px', opacity: 0.7, display: 'block', marginBottom: '4px' }}>
                  生まれた時間（不明の場合は空欄）
                </label>
                <input
                  type="number" min="0" max="23"
                  value={shiShuHour} onChange={(e) => setShiShuHour(e.target.value)}
                  placeholder="時刻（0-23）"
                  style={{ width: '100%', padding: '6px', background: '#333', border: '1px solid #555', borderRadius: '4px', color: '#fff', fontSize: '11px' }}
                />
              </div>

              <div style={{ marginBottom: '8px' }}>
                <label style={{ fontSize: '10px', opacity: 0.7, display: 'block', marginBottom: '4px' }}>性別</label>
                <select
                  value={shiShuGender} onChange={(e) => setShiShuGender(e.target.value)}
                  style={{ width: '100%', padding: '6px', background: '#333', border: '1px solid #555', borderRadius: '4px', color: '#fff', fontSize: '11px' }}
                >
                  <option value="不明">不明</option>
                  <option value="男">男</option>
                  <option value="女">女</option>
                </select>
              </div>

              <div style={{ marginBottom: '8px' }}>
                <label style={{ fontSize: '10px', opacity: 0.7, display: 'block', marginBottom: '4px' }}>
                  ご質問（オプション）
                </label>
                <input
                  type="text"
                  value={userQuery} onChange={(e) => setUserQuery(e.target.value)}
                  placeholder="今年の運勢は？"
                  style={{ width: '100%', padding: '6px', background: '#333', border: '1px solid #555', borderRadius: '4px', color: '#fff', fontSize: '11px' }}
                />
              </div>

              <button
                onClick={handleExecuteDivination}
                disabled={aiLoading}
                style={{
                  width: '100%', padding: '8px',
                  background: aiLoading ? '#666' : '#d4af37',
                  color: '#000', border: 'none', borderRadius: '4px',
                  fontSize: '11px', fontWeight: 'bold',
                  cursor: aiLoading ? 'not-allowed' : 'pointer',
                  opacity: aiLoading ? 0.5 : 1,
                }}
              >
                {aiLoading ? '鑑定中...' : '鑑定実行'}
              </button>

              {aiResult && (
                <div style={{
                  marginTop: '10px', padding: '8px',
                  background: '#1a1a1a', borderRadius: '4px', border: '1px solid #d4af37',
                }}>
                  <p style={{
                    fontSize: '10px',
                    color: aiResult.status === 'error' ? '#ff6b6b' : '#d4af37',
                    marginBottom: '6px', fontWeight: 'bold',
                  }}>
                    {aiResult.status === 'error' ? '❌ エラー' : '✨ 鑑定文'}
                  </p>
                  <p style={{ fontSize: '10px', lineHeight: '1.5', color: '#fff', margin: 0 }}>
                    {aiResult.divination}
                  </p>
                  {aiResult.hour_pillar_mode && (
                    <p style={{ fontSize: '9px', color: '#999', marginTop: '6px' }}>
                      モード: {aiResult.hour_pillar_mode} | {aiResult.mode === 'mock' ? 'テストモード' : 'API実行'}
                    </p>
                  )}
                </div>
              )}
            </div>
          )}

          {/* ════ 易占モード ════ */}
          {divinationMode === '易占' && (
            <div style={{
              marginBottom: '15px', padding: '10px',
              background: '#2a2a2a', borderRadius: '5px', border: '1px solid #555',
            }}>
              <h3 style={{ fontSize: '13px', marginBottom: '4px', color: '#d4af37', letterSpacing: '2px' }}>
                ☯ 易占
              </h3>
              <p style={{ fontSize: '10px', color: '#888', marginBottom: '12px', lineHeight: 1.6 }}>
                心を静めて問いを定め、ボタンを押してください。<br />
                六十四卦があなたへ答えを示します。
              </p>

              {/* 質問入力 */}
              <div style={{ marginBottom: '10px' }}>
                <label style={{ fontSize: '10px', opacity: 0.7, display: 'block', marginBottom: '4px' }}>
                  お伺いの内容（任意）
                </label>
                <input
                  type="text"
                  value={userQuery} onChange={(e) => setUserQuery(e.target.value)}
                  placeholder="例：この仕事を進めるべきか？"
                  style={{
                    width: '100%', padding: '6px', boxSizing: 'border-box',
                    background: '#333', border: '1px solid #555',
                    borderRadius: '4px', color: '#fff', fontSize: '11px',
                  }}
                />
              </div>

              {/* 実行ボタン */}
              <button
                onClick={handleYiDivination}
                style={{
                  width: '100%', padding: '10px',
                  background: 'linear-gradient(135deg, #d4af37, #8B6914)',
                  color: '#000', border: 'none', borderRadius: '5px',
                  fontSize: '12px', fontWeight: 'bold',
                  cursor: 'pointer', letterSpacing: '2px',
                  boxShadow: '0 0 12px rgba(212,175,55,0.4)',
                  marginBottom: '12px',
                }}
              >
                ☯ 易占を実行する
              </button>

              {/* 結果カード */}
              {divinationResult && (
                <div style={{
                  background: '#111',
                  border: `1px solid ${divinationResult.color}`,
                  borderRadius: '8px', padding: '12px',
                  boxShadow: `0 0 18px ${divinationResult.color}44`,
                }}>
                  {/* 卦シンボル・名前・吉凶バッジ */}
                  <div style={{ textAlign: 'center', marginBottom: '10px' }}>
                    <div style={{
                      fontSize: '44px', lineHeight: 1,
                      color: divinationResult.color, marginBottom: '6px',
                    }}>
                      {divinationResult.number}
                    </div>
                    <div style={{
                      fontSize: '16px', fontWeight: 'bold',
                      color: divinationResult.color, letterSpacing: '3px', marginBottom: '6px',
                    }}>
                      {divinationResult.name}
                    </div>
                    <div style={{
                      display: 'inline-block', padding: '2px 12px',
                      background: divinationResult.color, color: '#000',
                      borderRadius: '20px', fontSize: '11px', fontWeight: 'bold', letterSpacing: '1px',
                    }}>
                      {divinationResult.reading}
                    </div>
                  </div>

                  {/* キーワード */}
                  <div style={{
                    textAlign: 'center', fontSize: '10px',
                    color: '#aaa', letterSpacing: '1px', marginBottom: '10px',
                  }}>
                    {divinationResult.keyword}
                  </div>

                  {/* 区切り線（自己クローズ） */}
                  <div style={{ borderTop: `1px solid ${divinationResult.color}44`, marginBottom: '10px' }} />

                  {/* お伺いの内容 */}
                  {userQuery && (
                    <div style={{ marginBottom: '8px' }}>
                      <span style={{ fontSize: '9px', color: '#888' }}>【お伺い】</span>
                      <p style={{ fontSize: '10px', color: '#ccc', margin: '2px 0 0', fontStyle: 'italic' }}>
                        「{userQuery}」
                      </p>
                    </div>
                  )}

                  {/* 卦辞 */}
                  <div style={{ marginBottom: '8px' }}>
                    <span style={{ fontSize: '9px', color: '#888' }}>【卦辞】</span>
                    <p style={{ fontSize: '10px', color: '#fff', lineHeight: '1.6', margin: '4px 0 0' }}>
                      {divinationResult.message}
                    </p>
                  </div>

                  {/* 行動指針 */}
                  <div style={{
                    background: `${divinationResult.color}18`,
                    border: `1px solid ${divinationResult.color}55`,
                    borderRadius: '4px', padding: '6px 8px',
                  }}>
                    <span style={{ fontSize: '9px', color: divinationResult.color }}>✦ 指針　</span>
                    <span style={{ fontSize: '10px', color: '#fff', fontWeight: 'bold' }}>
                      {divinationResult.advice}
                    </span>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* ════ 風水鑑定モード ════ */}
          {divinationMode === '風水鑑定' && (
            <>
              <div style={{ marginBottom: '15px' }}>
                <label style={{ fontSize: '10px', opacity: 0.7 }}>表示層選択:</label>
                <select
                  value={activeLayer} onChange={(e) => setActiveLayer(e.target.value)}
                  style={{ width: '100%', background: '#333', color: '#fff', border: '1px solid #555', padding: '10px', borderRadius: '5px' }}
                >
                  {layers.map(layer => (
                    <option key={layer.id} value={layer.id}>{layer.id}（{layer.name}）</option>
                  ))}
                </select>
              </div>

              <div style={{ marginBottom: '15px' }}>
                <label style={{ fontSize: '10px', opacity: 0.7 }}>カメラ切り替え:</label>
                <CameraSelector onSelect={setSelectedCameraId} currentId={selectedCameraId} />
              </div>

              <div className="analysis-summary">
                <p><strong>L1:</strong>  {analyzed.L1}</p>
                <p><strong>L2:</strong>  {analyzed.L2}</p>
                <p><strong>L3:</strong>  {analyzed.L3}</p>
                <p><strong>L4:</strong>  {analyzed.L4}</p>
                <p><strong>L5:</strong>  {analyzed.L5}</p>
                <p><strong>L6:</strong>  {analyzed.L6}</p>
                <p><strong>L7:</strong>  {analyzed.L7}</p>
                <p><strong>L8:</strong>  {analyzed.L8}</p>
                <p><strong>L9:</strong>  {analyzed.L9}</p>
                <p><strong>L10:</strong> {analyzed.L10}</p>
                <p><strong>L11:</strong> {analyzed.L11}</p>
                <p><strong>L12:</strong> {analyzed.L12}</p>
                <p><strong>L13:</strong> {analyzed.L13}</p>
                <p><strong>L14:</strong> {analyzed.L14}</p>
                <p><strong>L15:</strong> {analyzed.L15}</p>
                <p><strong>L16:</strong> {analyzed.L16}</p>
                <p><strong>L17:</strong> {analyzed.L17}</p>
                <p><strong>L19:</strong> {analyzed.L19}</p>
                <p><strong>L20:</strong> {analyzed.L20}</p>
                <p style={{ color: analyzed.isImportant ? '#ff6b6b' : '#fff' }}>
                  <strong>重要:</strong> {analyzed.isImportant ? 'はい' : 'いいえ'}
                </p>
              </div>

              <div className="strength-row">
                <input
                  placeholder="備考（氏名など）"
                  value={note} onChange={e => setNote(e.target.value)}
                />
              </div>

              <button
                className="panel-btn"
                onClick={handleSave}
                disabled={saveStatus === 'loading'}
              >
                {saveStatus === 'loading'
                  ? '標高取得中...'
                  : saveStatus === 'success'
                  ? '✅ 保存完了'
                  : '💾 標高込みで保存'}
              </button>
            </>
          )}

        </div>
      </div>

      {/* レーザーライン（複数行自己クローズ div） */}
      <div
        onTouchMove={(e) => setLaserPos(e.touches[0].clientX)}
        style={{
          position: 'absolute',
          left: laserPos,
          top: 0,
          width: 2,
          height: '100%',
          background: 'red',
          boxShadow: '0 0 10px red',
          zIndex: 5,
        }}
      />

    </div>
  )
}

// ─────────────────────────────────────────────
// CameraSelector
// ─────────────────────────────────────────────
function CameraSelector({ onSelect, currentId }) {
  const [devices, setDevices] = useState([])
  useEffect(() => {
    navigator.mediaDevices.enumerateDevices().then(ds => {
      setDevices(ds.filter(d => d.kind === 'videoinput'))
    })
  }, [])
  return (
    <select
      value={currentId}
      onChange={(e) => onSelect(e.target.value)}
      style={{
        width: '100%', background: '#333', color: '#fff',
        border: '1px solid #555', padding: '10px', borderRadius: '5px',
      }}
    >
      <option value="">（デフォルト）</option>
      {devices.map(d => (
        <option key={d.deviceId} value={d.deviceId}>
          {d.label || `Camera ${d.deviceId.slice(0, 5)}`}
        </option>
      ))}
    </select>
  )
}

export default App