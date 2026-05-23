import { useState } from 'react';
import PropTypes from 'prop-types';
import Hexagram from './Hexagram';

function HistoryItem({ item, onUpdateFeedback }) {
  const [feedback, setFeedback] = useState(item.feedback || '');
  const [selfScore, setSelfScore] = useState(item.self_score ?? '');
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  const saveFeedback = async () => {
    setSaving(true);
    setMessage('');
    const result = await onUpdateFeedback(item.id, {
      feedback,
      self_score: selfScore === '' ? '' : Number(selfScore),
    });
    if (result.ok) {
      setMessage('保存しました。');
    } else {
      setMessage(result.message || '保存に失敗しました。');
    }
    setSaving(false);
  };

  return (
    <article className="history-card">
      <details className="history-collapse" open={item.id === 1}>
        <summary className="history-summary">
          <div className="history-summary-main">
            <strong>#{item.id} {item.person_name}</strong>
            <span className="history-time">{item.created_at}</span>
          </div>
          <div className="history-summary-category">カテゴリ: {item.category || '総合'}</div>
          <div className="history-summary-sub">{item.question}</div>
          <div className="history-summary-meta">
            <span>一致度: {item.self_score ?? '未評価'}</span>
            {item.evaluated_at && <span>評価: {item.evaluated_at}</span>}
          </div>
        </summary>

        <div className="history-collapse-body">
          <p className="history-question"><strong>質問:</strong> {item.question}</p>
          <p className="history-question"><strong>卦の意味要約:</strong> {item.hexagram_summary}</p>
          {item.evaluated_at && <p className="history-question"><strong>評価日時:</strong> {item.evaluated_at}</p>}

          <div className="history-hexagrams">
            <Hexagram hexagram={item.honke} changingLine={item.changing_line} label="本卦" />
            <Hexagram hexagram={item.shike} label="之卦" />
          </div>

          <section className="description-card">
            <p className="description-text"><strong>Gemini回答:</strong></p>
            <p className="description-text history-ai-text">{item.ai_response}</p>
          </section>

          <section className="history-feedback">
            <label htmlFor={`feedback-${item.id}`} className="input-label">後日フィードバック（実際の出来事・整合性）</label>
            <textarea
              id={`feedback-${item.id}`}
              className="text-input text-area"
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
              placeholder="例: 2週間後に面接が決まり、助言どおり準備したら通過した。"
            />

            <label htmlFor={`score-${item.id}`} className="input-label">一致度の自己評価（1〜5）</label>
            <select
              id={`score-${item.id}`}
              className="text-input score-select"
              value={selfScore}
              onChange={(e) => setSelfScore(e.target.value)}
            >
              <option value="">未評価</option>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
            </select>

            <button type="button" className="small-button" disabled={saving} onClick={saveFeedback}>
              {saving ? '保存中...' : 'フィードバックを保存'}
            </button>
            {message && <p className="history-message">{message}</p>}
          </section>
        </div>
      </details>
    </article>
  );
}

HistoryItem.propTypes = {
  item: PropTypes.shape({
    id: PropTypes.number.isRequired,
    person_name: PropTypes.string,
    question: PropTypes.string,
    created_at: PropTypes.string,
    changing_line: PropTypes.number,
    honke: PropTypes.object,
    shike: PropTypes.object,
    ai_response: PropTypes.string,
    feedback: PropTypes.string,
    self_score: PropTypes.number,
    evaluated_at: PropTypes.string,
    hexagram_summary: PropTypes.string,
    category: PropTypes.string,
  }).isRequired,
  onUpdateFeedback: PropTypes.func.isRequired,
};

function HistoryList({ histories, loading, onRefresh, onUpdateFeedback, filters, onSearch, onExportCsv, onExportSheets }) {
  const [localFilters, setLocalFilters] = useState(filters);

  const updateFilter = (key, value) => {
    setLocalFilters((prev) => ({ ...prev, [key]: value }));
  };

  const resetFilters = () => {
    const empty = {
      person_name: '',
      keyword: '',
      from_date: '',
      to_date: '',
      min_score: '',
      max_score: '',
    };
    setLocalFilters(empty);
    onSearch(empty);
  };

  return (
    <section className="result-section">
      <div className="history-filter-grid">
        <input
          className="text-input"
          placeholder="名前で検索"
          value={localFilters.person_name}
          onChange={(e) => updateFilter('person_name', e.target.value)}
        />
        <input
          className="text-input"
          placeholder="質問キーワード"
          value={localFilters.keyword}
          onChange={(e) => updateFilter('keyword', e.target.value)}
        />
        <input
          className="text-input"
          type="date"
          value={localFilters.from_date}
          onChange={(e) => updateFilter('from_date', e.target.value)}
        />
        <input
          className="text-input"
          type="date"
          value={localFilters.to_date}
          onChange={(e) => updateFilter('to_date', e.target.value)}
        />
        <select
          className="text-input score-select"
          value={localFilters.min_score}
          onChange={(e) => updateFilter('min_score', e.target.value)}
        >
          <option value="">最小スコア</option>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
        </select>
        <select
          className="text-input score-select"
          value={localFilters.max_score}
          onChange={(e) => updateFilter('max_score', e.target.value)}
        >
          <option value="">最大スコア</option>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
        </select>
      </div>

      <div className="history-toolbar">
        <h2 className="section-title">📚 履歴一覧</h2>
        <div className="history-toolbar-actions">
          <button type="button" className="small-button" onClick={() => onSearch(localFilters)} disabled={loading}>
            {loading ? '検索中...' : '検索'}
          </button>
          <button type="button" className="small-button" onClick={resetFilters} disabled={loading}>
            条件クリア
          </button>
          <button type="button" className="small-button" onClick={() => onExportCsv(localFilters)} disabled={loading}>
            CSV出力（Mac/Sheets）
          </button>
          <button type="button" className="small-button" onClick={() => onExportSheets(localFilters)} disabled={loading}>
            Google Sheetsへ転送
          </button>
          <button type="button" className="small-button" onClick={() => onRefresh(localFilters)} disabled={loading}>
            再読み込み
          </button>
        </div>
      </div>

      {!loading && histories.length === 0 && (
        <p className="divine-hint">履歴はまだありません。先に占いを実行してください。</p>
      )}

      <div className="history-list">
        {histories.map((item) => (
          <HistoryItem key={item.id} item={item} onUpdateFeedback={onUpdateFeedback} />
        ))}
      </div>
    </section>
  );
}

HistoryList.propTypes = {
  histories: PropTypes.arrayOf(PropTypes.object).isRequired,
  loading: PropTypes.bool.isRequired,
  onRefresh: PropTypes.func.isRequired,
  onUpdateFeedback: PropTypes.func.isRequired,
  filters: PropTypes.shape({
    person_name: PropTypes.string,
    keyword: PropTypes.string,
    from_date: PropTypes.string,
    to_date: PropTypes.string,
    min_score: PropTypes.string,
    max_score: PropTypes.string,
  }).isRequired,
  onSearch: PropTypes.func.isRequired,
  onExportCsv: PropTypes.func.isRequired,
  onExportSheets: PropTypes.func.isRequired,
};

export default HistoryList;
