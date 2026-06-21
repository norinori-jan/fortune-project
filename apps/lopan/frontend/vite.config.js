import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import basicSsl from '@vitejs/plugin-basic-ssl'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    basicSsl() // iPhoneのカメラ・方位計（Sensor）を動かすためのプラグイン（HTTPS時のみ有効）
  ],
  base: '/fengshui-app/', // GitHub PagesのURLパスに合わせる設定
  server: {
    host: true,     // スマホ（iPhone）からアクセス可能にする
    port: 5173,     // Viteのポート
    https: false,   // ← 一時的にHTTPに戻す（証明書問題を回避）
    cors: true,     // iPhoneからのアクセスを許可
    strictPort: true
  }
})
