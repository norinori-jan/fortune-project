/**
 * reading.js
 * DivinationReading 共通インターフェース
 * ReadingBridge：各ツールの生結果を共通型に変換・統合する
 *
 * 全ツールはこのファイルを通じてデータを交換する。
 * 直接のツール間データ受け渡しは禁止。
 */

import { WUXING, wuxingRelation } from './cosmology.js';
import { getCurrentTimeContext } from './timeAxis.js';

// ─────────────────────────────────────────────
// DivinationReading 型定義（JSDoc）
// ─────────────────────────────────────────────

/**
 * @typedef {Object} WuxingVector
 * @property {number} wood  - 0.0〜1.0
 * @property {number} fire
 * @property {number} earth
 * @property {number} metal
 * @property {number} water
 */

/**
 * @typedef {Object} DivinationReading
 * @property {'iching'|'tarot'|'lopan'|'kuzuu'} tool
 * @property {number}        timestamp
 * @property {WuxingVector}  wuxing
 * @property {object}        timeContext
 * @property {object}        reading
 * @property {string}        reading.core    - 核心メッセージ（50字以内）
 * @property {string}        reading.detail  - 詳細解釈
 * @property {string}        reading.action  - 推奨アクション
 * @property {string[]}      symbols
 * @property {object}        [resonance]
 * @property {string}        resonance.suggestedTool
 * @property {string}        resonance.reason
 * @property {object}        [rawResult]     - 元データ（デバッグ用）
 */

// ─────────────────────────────────────────────
// 空の WuxingVector を生成する
// ─────────────────────────────────────────────
export function emptyWuxing() {
  return { wood: 0, fire: 0, earth: 0, metal: 0, water: 0 };
}

/**
 * WuxingVector を正規化（合計が1.0になるよう）
 * @param {WuxingVector} v
 * @returns {WuxingVector}
 */
export function normalizeWuxing(v) {
  const total = Object.values(v).reduce((s, x) => s + x, 0);
  if (total === 0) return { wood: 0.2, fire: 0.2, earth: 0.2, metal: 0.2, water: 0.2 };
  return Object.fromEntries(Object.entries(v).map(([k, val]) => [k, val / total]));
}

/**
 * スコア（-2〜+6）を WuxingVector に変換するユーティリティ
 * 用神の五行が高い値を取るように設定する
 * @param {string} dominantWuxing - 最も強い五行
 * @param {number} score          - -2〜6
 * @returns {WuxingVector}
 */
export function scoreToWuxing(dominantWuxing, score) {
  const v = emptyWuxing();
  const normalized = Math.max(0, Math.min(1, (score + 2) / 8));
  v[dominantWuxing] = normalized;
  // 残りは均等配分
  const rest = (1 - normalized) / 4;
  Object.keys(v).forEach(k => { if (k !== dominantWuxing) v[k] = rest; });
  return v;
}

// ─────────────────────────────────────────────
// ReadingBridge
// ─────────────────────────────────────────────

export class ReadingBridge {
  static #adapters = {};
  static #history  = [];

  /**
   * アダプターを登録する
   * @param {'iching'|'tarot'|'lopan'|'kuzuu'} toolName
   * @param {function} adapterFn - rawResult → DivinationReading
   */
  static register(toolName, adapterFn) {
    this.#adapters[toolName] = adapterFn;
    console.info(`[ReadingBridge] ${toolName} アダプター登録完了`);
  }

  /**
   * 生結果を DivinationReading に変換する
   * @param {object} rawResult
   * @param {'iching'|'tarot'|'lopan'|'kuzuu'} toolName
   * @returns {DivinationReading}
   */
  static convert(rawResult, toolName) {
    const adapter = this.#adapters[toolName];
    if (!adapter) throw new Error(`[ReadingBridge] "${toolName}" のアダプターが未登録`);
    const reading = adapter(rawResult);
    this.#history.push(reading);
    return reading;
  }

  /**
   * 複数ツールの DivinationReading を統合して五行バランスを返す
   * @param {DivinationReading[]} readings
   * @returns {{ wuxing: WuxingVector, dominantWuxing: string, summary: string }}
   */
  static synthesize(readings) {
    if (readings.length === 0) {
      return { wuxing: emptyWuxing(), dominantWuxing: 'earth', summary: '読み解き結果がありません。' };
    }

    // 五行合算
    const sum = readings.reduce((acc, r) => {
      Object.keys(acc).forEach(k => { acc[k] += r.wuxing[k] ?? 0; });
      return acc;
    }, emptyWuxing());

    const normalized = normalizeWuxing(sum);
    const dominantWuxing = Object.entries(normalized)
      .sort(([, a], [, b]) => b - a)[0][0];

    // 欠けている五行を検出
    const lacking = Object.entries(normalized)
      .filter(([, v]) => v < 0.1)
      .map(([k]) => ({ wood: '木', fire: '火', earth: '土', metal: '金', water: '水' }[k]));

    const summary = lacking.length > 0
      ? `${lacking.join('・')}の気が不足しています。意識的に補うことが有効です。`
      : '五行のバランスは安定しています。';

    return { wuxing: normalized, dominantWuxing, summary };
  }

  /**
   * 直近の DivinationReading を取得する
   * @param {'iching'|'tarot'|'lopan'|'kuzuu'} [toolName]
   * @returns {DivinationReading|null}
   */
  static getLatest(toolName) {
    const filtered = toolName
      ? this.#history.filter(r => r.tool === toolName)
      : this.#history;
    return filtered[filtered.length - 1] ?? null;
  }

  /**
   * 履歴をすべて取得する
   * @returns {DivinationReading[]}
   */
  static getHistory() {
    return [...this.#history];
  }

  /**
   * 履歴をクリアする
   */
  static clearHistory() {
    this.#history = [];
  }

  /**
   * 次に勧めるツールを判定する（レゾナンス）
   * @param {DivinationReading} reading
   * @returns {{ suggestedTool: string, reason: string }}
   */
  static suggestResonance(reading) {
    const dominant = Object.entries(reading.wuxing)
      .sort(([, a], [, b]) => b - a)[0][0];

    // 五行と推奨ツールのマッピング
    const resonanceMap = {
      wood:  { tool: 'iching',  reason: '木の気は変化・成長を示します。易で流れの方向を確認しましょう。' },
      fire:  { tool: 'tarot',   reason: '火の気は直感・情熱を示します。タロットで心の声を聴きましょう。' },
      earth: { tool: 'lopan',   reason: '土の気は場所・安定を示します。風水で環境を整えましょう。' },
      metal: { tool: 'lopan',   reason: '金の気は精密さ・収縮を示します。羅盤で方位を確認しましょう。' },
      water: { tool: 'iching',  reason: '水の気は流動・知恵を示します。易で底流を読み解きましょう。' },
    };

    const suggestion = resonanceMap[dominant];
    // 既に同じツールならタロットを勧める
    if (suggestion.tool === reading.tool) {
      return { suggestedTool: 'tarot', reason: '異なる視点から心の状態を確認しましょう。' };
    }
    return { suggestedTool: suggestion.tool, reason: suggestion.reason };
  }
}

// ─────────────────────────────────────────────
// 永続化（Google Sheets Apps Script 連携）
// ─────────────────────────────────────────────

/**
 * DivinationReading を Apps Script エンドポイントに保存する
 * @param {DivinationReading} reading
 * @param {string} endpointUrl - Apps Script Web App URL
 * @returns {Promise<{ success: boolean, id: string }>}
 */
export async function saveReading(reading, endpointUrl) {
  if (!endpointUrl) {
    console.warn('[saveReading] エンドポイントURLが未設定。ローカル保存のみ。');
    _saveLocal(reading);
    return { success: false, id: null };
  }

  try {
    const res = await fetch(endpointUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...reading,
        rawResult: undefined, // 送信サイズ削減
      }),
    });
    const json = await res.json();
    _saveLocal(reading);
    return { success: true, id: json.id };
  } catch (err) {
    console.error('[saveReading] 保存失敗:', err);
    _saveLocal(reading);
    return { success: false, id: null };
  }
}

/** IndexedDB への簡易保存（オフラインフォールバック） */
function _saveLocal(reading) {
  try {
    const key = `reading_${reading.tool}_${reading.timestamp}`;
    // localStorage は artifact 環境では使えないため、
    // 実アプリでは idb-keyval 等を使うこと
    if (typeof localStorage !== 'undefined') {
      const existing = JSON.parse(localStorage.getItem('fortune_readings') || '[]');
      existing.push(reading);
      // 最新50件のみ保持
      localStorage.setItem('fortune_readings', JSON.stringify(existing.slice(-50)));
    }
  } catch (_) { /* noop */ }
}

// ─────────────────────────────────────────────
// ナビゲーション（アプリ間遷移）
// ─────────────────────────────────────────────

/**
 * 別ツールへのレゾナンス遷移を実行する
 * @param {DivinationReading} reading
 * @param {string} baseUrl - apps/ ディレクトリのベースURL
 */
export function navigateToResonance(reading, baseUrl = '..') {
  const { suggestedTool, reason } = ReadingBridge.suggestResonance(reading);
  try {
    sessionStorage.setItem('incoming_reading', JSON.stringify(reading));
  } catch (_) { /* noop */ }
  window.location.href = `${baseUrl}/${suggestedTool}/index.html?from=resonance`;
}

/**
 * 遷移先で incoming_reading を受け取る
 * @returns {DivinationReading|null}
 */
export function receiveIncomingReading() {
  try {
    const raw = sessionStorage.getItem('incoming_reading');
    if (!raw) return null;
    sessionStorage.removeItem('incoming_reading');
    return JSON.parse(raw);
  } catch (_) {
    return null;
  }
}
