import React, { useEffect, useRef } from 'react'

function CameraView({ videoRef, deviceId }) {
  const streamRef = useRef(null)

  useEffect(() => {
    const start = async () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(t => t.stop())
      }

      const constraints = {
        video: deviceId 
          ? { deviceId: { exact: deviceId } } 
          : { facingMode: { exact: 'environment' } } // iPhoneの背面レンズを強制
      }

      try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints)
        streamRef.current = stream
        if (videoRef.current) {
          videoRef.current.srcObject = stream
          videoRef.current.setAttribute("playsinline", true)
          videoRef.current.play()
        }
      } catch (err) {
        console.error("Camera起動エラー:", err)
        // 強制背面がダメな場合、通常の背面指定でリトライ
        if (!deviceId) {
          const fallback = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
          streamRef.current = fallback
          if (videoRef.current) videoRef.current.srcObject = fallback
        }
      }
    }
    start()
    return () => streamRef.current?.getTracks().forEach(t => t.stop())
  }, [deviceId])

  return (
    <div className="camera-layer">
      <video ref={videoRef} className="camera-preview" autoPlay playsInline muted />
    </div>
  )
}

export default CameraView