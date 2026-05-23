import { useCallback, useEffect, useMemo, useState } from 'react';
import DivinationResult from './components/DivinationResult';
import HistoryList from './components/HistoryList';
import AnalysisPanel from './components/AnalysisPanel';
import './App.css';

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '');
const LOCAL_HISTORY_KEY = 'fortune.histories.cache.v1';
const LOCAL_TREND_KEY = 'fortune.trend.cache.v1';
const LOCAL_CATEGORY_KEY = 'fortune.category.cache.v1';
const LOCAL_PENDING_UPDATES_KEY = 'fortune.pending.feedback.v1';
const LOCAL_PENDING_DIVINATIONS_KEY = 'fortune.pending.divinations.v1';

const apiUrl = (path) => {
  if (!API_BASE_URL) return path;
  return `${API_BASE_URL}${path}`;
};

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [rolling, setRolling] = useState(false);
  const [personName, setPersonName] = useState('');
  const [question, setQuestion] = useState('');
  const [histories, setHistories] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [view, setView] = useState('divine');
  const [trendGroup, setTrendGroup] = useState('weekly');
  const [trendData, setTrendData] = useState([]);
  const [categoryStats, setCategoryStats] = useState([]);
  const [trendLoading, setTrendLoading] = useState(false);
  const [concernType, setConcernType] = useState('総合');
  const [historyFilters, setHistoryFilters] = useState({
    person_name: '',
    keyword: '',
    from_date: '',
    to_date: '',
    min_score: '',
    max_score: '',
  });

  const persistLocal = (key, value) => {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch {
      // ストレージ上限やプライベートモードでは失敗しうる
    }
  };

  const readLocal = (key, fallback = null) => {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch {
      return fallback;
    }
  };

  const buildQueryString = (filters) => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== '' && value !== null && value !== undefined) {
        params.set(key, value);
      }
    });
    return params.toString();
  };

  const concernTemplates = useMemo(() => ({
    総合: '今の流れを総合的に見て、最優先で整えるべきことは何か。',
    恋愛: 'この関係を前進させるために、私が先に変えるべき行動は何か。',
    仕事: '仕事の成果を上げるために、今月やめるべき習慣は何か。',
    転職: '転職を進めるなら、動く時期と準備の優先順位はどうか。',
    金運: '支出と収入の流れを改善するために、今すぐ見直すべき点は何か。',
    人間関係: '対人ストレスを減らし信頼を増やすために取るべき姿勢は何か。',
    健康: '生活リズムを整えるうえで、最初に固定すべき行動は何か。',
    学業: '学習効率を上げるための学び方と時間配分の要点は何か。',
    家庭: '家庭内の空気をよくするために、私が変えるべき伝え方は何か。',
  }), []);

  const applyTemplate = () => {
    setQuestion(concernTemplates[concernType] || '');
  };

  useEffect(() => {
    const vv = window.visualViewport;
    if (!vv) return () => {};

    const onResize = () => {
      const keyboardOpen = vv.height < window.innerHeight * 0.78;
      document.body.classList.toggle('keyboard-open', keyboardOpen);
    };

    vv.addEventListener('resize', onResize);
    onResize();

    return () => {
      vv.removeEventListener('resize', onResize);
      document.body.classList.remove('keyboard-open');
    };
  }, []);

  useEffect(() => {
    // iOS実機でキーボード表示時に入力欄が隠れやすいので、軽く中央へスクロールする
    const onFocusIn = (event) => {
      const target = event.target;
      if (!(target instanceof HTMLElement)) return;
      if (!target.matches('input, textarea, select')) return;
      window.setTimeout(() => {
        target.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 120);
    };

    document.addEventListener('focusin', onFocusIn);
    return () => document.removeEventListener('focusin', onFocusIn);
  }, []);

  const syncPendingFeedbackUpdates = useCallback(async () => {
    const queue = readLocal(LOCAL_PENDING_UPDATES_KEY, []);
    if (!Array.isArray(queue) || queue.length === 0) return;

    const remains = [];
    for (const item of queue) {
      try {
        let response = await fetch(apiUrl(`/api/divinations/${item.id}`), {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(item.payload),
        });
        if (response.status === 404) {
          response = await fetch(`http://127.0.0.1:5000/api/divinations/${item.id}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(item.payload),
          });
        }
        if (!response.ok) {
          remains.push(item);
        }
      } catch {
        remains.push(item);
      }
    }
    persistLocal(LOCAL_PENDING_UPDATES_KEY, remains);
  }, []);

  const postDivination = useCallback(async (payload) => {
    let response = await fetch(apiUrl('/api/divine'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (response.status === 404) {
      response = await fetch('http://127.0.0.1:5000/api/divine', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
    }
    if (!response.ok) {
      throw new Error(`サーバーエラー: ${response.status}`);
    }
    return response.json();
  }, []);

  const syncPendingDivinations = useCallback(async () => {
    const queue = readLocal(LOCAL_PENDING_DIVINATIONS_KEY, []);
    if (!Array.isArray(queue) || queue.length === 0) return;

    const remains = [];
    let syncedCount = 0;
    for (const item of queue) {
      try {
        await postDivination(item.payload);
        syncedCount += 1;
      } catch {
        remains.push(item);
      }
    }
    persistLocal(LOCAL_PENDING_DIVINATIONS_KEY, remains);

    if (syncedCount > 0) {
      setError(`オフライン保存していた占い ${syncedCount} 件を送信しました。`);
    }
  }, [postDivination]);

  useEffect(() => {
    const cachedHistories = readLocal(LOCAL_HISTORY_KEY, []);
    const cachedTrend = readLocal(LOCAL_TREND_KEY, []);
    const cachedCategory = readLocal(LOCAL_CATEGORY_KEY, []);

    if (Array.isArray(cachedHistories) && cachedHistories.length > 0) {
      setHistories(cachedHistories);
    }
    if (Array.isArray(cachedTrend) && cachedTrend.length > 0) {
      setTrendData(cachedTrend);
    }
    if (Array.isArray(cachedCategory) && cachedCategory.length > 0) {
      setCategoryStats(cachedCategory);
    }

    syncPendingFeedbackUpdates();
    syncPendingDivinations();
    const onOnline = () => {
      syncPendingFeedbackUpdates();
      syncPendingDivinations();
    };
    window.addEventListener('online', onOnline);
    return () => {
      window.removeEventListener('online', onOnline);
    };
  }, [syncPendingFeedbackUpdates, syncPendingDivinations]);

  const fetchTrend = async (group = trendGroup) => {
    setTrendLoading(true);
    setError(null);
    setTrendGroup(group);
    try {
      let response = await fetch(apiUrl(`/api/divinations/stats/trend?group=${group}`));
      if (response.status === 404) {
        response = await fetch(`http://127.0.0.1:5000/api/divinations/stats/trend?group=${group}`);
      }
      if (!response.ok) {
        throw new Error(`分析取得エラー: ${response.status}`);
      }
      const data = await response.json();
      setTrendData(data);
      persistLocal(LOCAL_TREND_KEY, data);
    } catch (err) {
      const cached = readLocal(LOCAL_TREND_KEY, []);
      if (Array.isArray(cached) && cached.length > 0) {
        setTrendData(cached);
        setError('オフラインのため、端末に保存した分析データを表示しています。');
      } else {
        setError(err.message || '分析データの取得に失敗しました。');
      }
    } finally {
      setTrendLoading(false);
    }
  };

  const fetchCategoryStats = async (filters = historyFilters) => {
    const qs = buildQueryString(filters);
    const suffix = qs ? `?${qs}` : '';
    try {
      let response = await fetch(apiUrl(`/api/divinations/stats/categories${suffix}`));
      if (response.status === 404) {
        response = await fetch(`http://127.0.0.1:5000/api/divinations/stats/categories${suffix}`);
      }
      if (!response.ok) {
        throw new Error(`カテゴリ分析取得エラー: ${response.status}`);
      }
      const data = await response.json();
      setCategoryStats(data);
      persistLocal(LOCAL_CATEGORY_KEY, data);
    } catch (err) {
      const cached = readLocal(LOCAL_CATEGORY_KEY, []);
      if (Array.isArray(cached) && cached.length > 0) {
        setCategoryStats(cached);
      } else {
        setError(err.message || 'カテゴリ分析データの取得に失敗しました。');
      }
    }
  };

  const fetchHistories = async (filters = historyFilters) => {
    setHistoryFilters(filters);
    setHistoryLoading(true);
    setError(null);
    const qs = buildQueryString(filters);
    const suffix = qs ? `?${qs}` : '';
    try {
      let response = await fetch(apiUrl(`/api/divinations${suffix}`));
      if (response.status === 404) {
        response = await fetch(`http://127.0.0.1:5000/api/divinations${suffix}`);
      }
      if (!response.ok) {
        throw new Error(`履歴取得エラー: ${response.status}`);
      }
      const data = await response.json();
      setHistories(data);
      persistLocal(LOCAL_HISTORY_KEY, data);
    } catch (err) {
      const cached = readLocal(LOCAL_HISTORY_KEY, []);
      if (Array.isArray(cached) && cached.length > 0) {
        setHistories(cached);
        setError('オフラインのため、端末に保存した履歴を表示しています。');
      } else {
        setError(err.message || '履歴の取得に失敗しました。');
      }
    } finally {
      setHistoryLoading(false);
    }
  };

  const updateFeedback = async (id, payload) => {
    try {
      let response = await fetch(apiUrl(`/api/divinations/${id}`), {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (response.status === 404) {
        response = await fetch(`http://127.0.0.1:5000/api/divinations/${id}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
      }
      if (!response.ok) {
        throw new Error(`フィードバック更新エラー: ${response.status}`);
      }
      const updated = await response.json();
      setHistories((prev) => {
        const next = prev.map((h) => (h.id === id ? updated : h));
        persistLocal(LOCAL_HISTORY_KEY, next);
        return next;
      });
      if (result?.id === id) {
        setResult(updated);
      }
      return { ok: true };
    } catch (err) {
      // オフライン時は端末キャッシュだけ先に更新し、オンライン復帰で再同期する
      setHistories((prev) => {
        const next = prev.map((h) => (h.id === id ? { ...h, ...payload, pending_sync: true } : h));
        persistLocal(LOCAL_HISTORY_KEY, next);
        return next;
      });
      const queue = readLocal(LOCAL_PENDING_UPDATES_KEY, []);
      const nextQueue = Array.isArray(queue) ? [...queue, { id, payload }] : [{ id, payload }];
      persistLocal(LOCAL_PENDING_UPDATES_KEY, nextQueue);
      return { ok: false, message: err.message || '更新に失敗しました。' };
    }
  };

  const exportHistoriesCsv = async (filters = historyFilters) => {
    const qs = buildQueryString(filters);
    const suffix = qs ? `?${qs}` : '';
    const candidates = [
      apiUrl(`/api/divinations/export.csv${suffix}`),
      `http://127.0.0.1:5000/api/divinations/export.csv${suffix}`,
    ];

    for (const url of candidates) {
      try {
        const response = await fetch(url);
        if (!response.ok) continue;
        const blob = await response.blob();
        const objectUrl = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = objectUrl;
        a.download = `divinations_${new Date().toISOString().slice(0, 19).replace(/[:T]/g, '-')}.csv`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(objectUrl);
        return;
      } catch {
        // 次候補へフォールバック
      }
    }
    setError('CSVエクスポートに失敗しました。');
  };

  const exportHistoriesToSheets = async (filters = historyFilters) => {
    const body = {
      filters,
    };

    const candidates = [
      apiUrl('/api/divinations/export/sheets'),
      'http://127.0.0.1:5000/api/divinations/export/sheets',
    ];

    for (const url of candidates) {
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
        });
        if (!response.ok) {
          continue;
        }
        const data = await response.json();
        setError(null);
        alert(`Googleスプレッドシートへ転送しました（${data.row_count}件）`);
        return;
      } catch {
        // 次候補へ
      }
    }

    setError('Googleスプレッドシート転送に失敗しました。設定値を確認してください。');
  };

  const handleDivine = async () => {
    setRolling(true);
    setError(null);

    // サイコロを振るアニメーション（500ms）
    await new Promise((res) => setTimeout(res, 500));
    setRolling(false);
    setLoading(true);

    try {
      const normalizedQuestion = question.trim() || concernTemplates[concernType];
      const composedQuestion = `【${concernType}】 ${normalizedQuestion}`;
      const payload = {
        person_name: personName,
        question: composedQuestion,
        concern_type: concernType,
      };

      const data = await postDivination(payload);
      setResult(data);
      fetchHistories();
      fetchCategoryStats(historyFilters);
    } catch (err) {
      const allowQueue = window.confirm(
        '現在オフラインの可能性があります。今回の占い内容を端末に一時保存し、オンライン復帰後に自動送信しますか？',
      );

      if (allowQueue) {
        const normalizedQuestion = question.trim() || concernTemplates[concernType];
        const composedQuestion = `【${concernType}】 ${normalizedQuestion}`;
        const queue = readLocal(LOCAL_PENDING_DIVINATIONS_KEY, []);
        const nextQueue = Array.isArray(queue)
          ? [...queue, {
            queued_at: new Date().toISOString(),
            payload: {
              person_name: personName,
              question: composedQuestion,
              concern_type: concernType,
            },
          }]
          : [{
            queued_at: new Date().toISOString(),
            payload: {
              person_name: personName,
              question: composedQuestion,
              concern_type: concernType,
            },
          }];
        persistLocal(LOCAL_PENDING_DIVINATIONS_KEY, nextQueue);
        setError('占い内容を端末に一時保存しました。オンライン復帰後に自動送信します。');
      } else {
        setError(err.message || '占いに失敗しました。バックエンドが起動しているか確認してください。');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1 className="app-title">☯ 易占い（周易）</h1>
        <p className="app-subtitle">六十四卦で運命を読む</p>
      </header>

      <main className="app-main">
        <div className="mode-switch" role="tablist" aria-label="表示モード">
          <button
            type="button"
            className={`mode-button ${view === 'divine' ? 'active' : ''}`}
            onClick={() => setView('divine')}
          >
            占い
          </button>
          <button
            type="button"
            className={`mode-button ${view === 'history' ? 'active' : ''}`}
            onClick={() => {
              setView('history');
              fetchHistories(historyFilters);
            }}
          >
            履歴一覧
          </button>
          <button
            type="button"
            className={`mode-button ${view === 'analysis' ? 'active' : ''}`}
            onClick={() => {
              setView('analysis');
              fetchTrend(trendGroup);
              fetchCategoryStats(historyFilters);
            }}
          >
            分析
          </button>
        </div>

        {view === 'divine' && (
          <div className="input-grid">
            <label className="input-label" htmlFor="personName">占った人の名前</label>
            <input
              id="personName"
              className="text-input"
              type="text"
              value={personName}
              onChange={(e) => setPersonName(e.target.value)}
              placeholder="例: 山田 太郎"
            />

            <label className="input-label" htmlFor="question">占いたい内容</label>
            <select
              id="concernType"
              className="text-input"
              value={concernType}
              onChange={(e) => setConcernType(e.target.value)}
            >
              {Object.keys(concernTemplates).map((key) => (
                <option key={key} value={key}>{key}</option>
              ))}
            </select>
            <button type="button" className="small-button" onClick={applyTemplate}>
              テンプレ質問を入れる
            </button>
            <textarea
              id="question"
              className="text-input text-area"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="例: 今月の仕事運と注意点"
            />
          </div>
        )}

        <div className="divine-section">
          {view === 'divine' && (
          <button
            className={`divine-button ${rolling ? 'rolling' : ''}`}
            onClick={handleDivine}
            disabled={loading || rolling}
          >
            {rolling ? '🎲 🎲 🎲' : loading ? '占い中...' : '🎲 占う'}
          </button>
          )}
          <p className="divine-hint">ボタンを押してサイコロを振り、卦を立ててください</p>
        </div>

        {error && (
          <div className="error-banner">
            <strong>エラー:</strong> {error}
          </div>
        )}

        {view === 'divine' && result && !loading && <DivinationResult result={result} />}
        {view === 'history' && (
          <HistoryList
            histories={histories}
            loading={historyLoading}
            onRefresh={fetchHistories}
            onUpdateFeedback={updateFeedback}
            filters={historyFilters}
            onSearch={fetchHistories}
            onExportCsv={exportHistoriesCsv}
            onExportSheets={exportHistoriesToSheets}
          />
        )}
        {view === 'analysis' && (
          <AnalysisPanel
            loading={trendLoading}
            trendGroup={trendGroup}
            trendData={trendData}
            categoryStats={categoryStats}
            onChangeGroup={fetchTrend}
            onRefresh={() => {
              fetchTrend(trendGroup);
              fetchCategoryStats(historyFilters);
            }}
          />
        )}
      </main>

      <nav className="bottom-nav" aria-label="スマホ下部ナビ">
        <button
          type="button"
          className={`bottom-nav-button ${view === 'divine' ? 'active' : ''}`}
          onClick={() => setView('divine')}
        >
          占い
        </button>
        <button
          type="button"
          className={`bottom-nav-button ${view === 'history' ? 'active' : ''}`}
          onClick={() => {
            setView('history');
            fetchHistories(historyFilters);
          }}
        >
          履歴
        </button>
        <button
          type="button"
          className={`bottom-nav-button ${view === 'analysis' ? 'active' : ''}`}
          onClick={() => {
            setView('analysis');
            fetchTrend(trendGroup);
            fetchCategoryStats(historyFilters);
          }}
        >
          分析
        </button>
      </nav>

      <footer className="app-footer">
        <p>易（周易）— 変化の書 | 八卦×八卦 = 六十四卦</p>
      </footer>
    </div>
  );
}

export default App;
