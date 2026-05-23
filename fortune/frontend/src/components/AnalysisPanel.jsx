import PropTypes from 'prop-types';

function AnalysisPanel({ loading, trendGroup, trendData, categoryStats, onChangeGroup, onRefresh }) {
  const maxCount = Math.max(...trendData.map((d) => d.evaluated_count), 1);
  const latest = trendData.length > 0 ? trendData[trendData.length - 1] : null;
  const maxCategoryCount = Math.max(...categoryStats.map((d) => d.evaluated_count), 1);

  return (
    <section className="result-section analysis-panel">
      <div className="history-toolbar">
        <h2 className="section-title">📈 一致度分析</h2>
        <div className="history-toolbar-actions">
          <button
            type="button"
            className={`small-button ${trendGroup === 'weekly' ? 'active-chip' : ''}`}
            onClick={() => onChangeGroup('weekly')}
            disabled={loading}
          >
            週次
          </button>
          <button
            type="button"
            className={`small-button ${trendGroup === 'monthly' ? 'active-chip' : ''}`}
            onClick={() => onChangeGroup('monthly')}
            disabled={loading}
          >
            月次
          </button>
          <button type="button" className="small-button" onClick={onRefresh} disabled={loading}>
            {loading ? '集計中...' : '再集計'}
          </button>
        </div>
      </div>

      {latest && (
        <div className="analysis-kpi-grid">
          <div className="kpi-card">
            <p className="kpi-label">最新期間</p>
            <p className="kpi-value">{latest.period}</p>
          </div>
          <div className="kpi-card">
            <p className="kpi-label">平均一致度</p>
            <p className="kpi-value">{latest.avg_score ?? '-'} / 5</p>
          </div>
          <div className="kpi-card">
            <p className="kpi-label">評価件数</p>
            <p className="kpi-value">{latest.evaluated_count}</p>
          </div>
        </div>
      )}

      {trendData.length === 0 && !loading && (
        <p className="divine-hint">まだ評価データがありません。履歴画面で自己評価スコアを入力してください。</p>
      )}

      <div className="trend-list">
        {trendData.map((row) => (
          <div key={row.period} className="trend-row">
            <div className="trend-head">
              <strong>{row.period}</strong>
              <span>平均 {row.avg_score ?? '-'} / 5（{row.evaluated_count}件）</span>
            </div>
            <div className="trend-bar-wrap" aria-label={`${row.period} の評価件数バー`}>
              <div className="trend-bar" style={{ width: `${(row.evaluated_count / maxCount) * 100}%` }} />
            </div>
          </div>
        ))}
      </div>

      <h3 className="section-subtitle">カテゴリ別 一致度比較</h3>
      {categoryStats.length === 0 && !loading && (
        <p className="divine-hint">カテゴリ比較に必要な評価データがありません。</p>
      )}
      <div className="trend-list">
        {categoryStats.map((row) => (
          <div key={row.category} className="trend-row">
            <div className="trend-head">
              <strong>{row.category}</strong>
              <span>平均 {row.avg_score ?? '-'} / 5（{row.evaluated_count}件）</span>
            </div>
            <div className="trend-bar-wrap" aria-label={`${row.category} の評価件数バー`}>
              <div className="trend-bar" style={{ width: `${(row.evaluated_count / maxCategoryCount) * 100}%` }} />
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

AnalysisPanel.propTypes = {
  loading: PropTypes.bool.isRequired,
  trendGroup: PropTypes.oneOf(['weekly', 'monthly']).isRequired,
  trendData: PropTypes.arrayOf(
    PropTypes.shape({
      period: PropTypes.string,
      evaluated_count: PropTypes.number,
      avg_score: PropTypes.number,
      min_score: PropTypes.number,
      max_score: PropTypes.number,
    }),
  ).isRequired,
  categoryStats: PropTypes.arrayOf(
    PropTypes.shape({
      category: PropTypes.string,
      evaluated_count: PropTypes.number,
      avg_score: PropTypes.number,
      min_score: PropTypes.number,
      max_score: PropTypes.number,
    }),
  ).isRequired,
  onChangeGroup: PropTypes.func.isRequired,
  onRefresh: PropTypes.func.isRequired,
};

export default AnalysisPanel;
