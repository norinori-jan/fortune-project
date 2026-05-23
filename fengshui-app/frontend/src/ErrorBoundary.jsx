import { Component } from 'react'

class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, errorMessage: '' }
  }

  static getDerivedStateFromError(error) {
    return {
      hasError: true,
      errorMessage: error?.message || '不明なエラーが発生しました。',
    }
  }

  componentDidCatch(error, info) {
    console.error('ErrorBoundary captured:', error, info)
  }

  handleRetry = () => {
    this.setState({ hasError: false, errorMessage: '' })
    if (this.props.onRetry) {
      this.props.onRetry()
    }
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-screen">
          <h1>⚠️ 画面でエラーが発生しました</h1>
          <p>iPhoneの設定を確認してください。</p>
          <p>Safari: 設定 → Safari → 位置情報/モーションと方向のアクセス を許可してください。</p>
          <p>カメラ許可が拒否されている場合は、設定 → Safari → カメラ で許可に変更してください。</p>
          <ul className="error-checklist">
            <li>Codespaces の 5000 番ポートが Public になっているか確認してください。</li>
            <li>フロント(5173) と API(5000) の URL が同じ Codespaces ワークスペースか確認してください。</li>
            <li>API サーバーが起動中か確認してください（app.py）。</li>
            <li>iPhone が同じネットワークで、VPN などで遮断されていないか確認してください。</li>
          </ul>
          <p className="error-detail">{this.state.errorMessage}</p>
          <button type="button" className="primary-btn" onClick={this.handleRetry}>
            再試行
          </button>
        </div>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary