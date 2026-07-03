/**
 * app.js — タロット鑑定アプリ メインロジック（完全版・省略なし）
 *
 * 依存:
 *   - js/cards_data.js  → グローバル変数 TAROT_DATA (Array, 22枚)
 *   - registry/spreads.json → SPREADS_DATA (fetch で読み込み、またはグローバル注入)
 *
 * TAROT_DATA の各要素フォーマット想定:
 * {
 *   id: 0,
 *   name: "愚者",
 *   name_en: "The Fool",
 *   keywords_upright: ["自由", "冒険", "無限の可能性"],
 *   keywords_reversed: ["無謀", "無計画", "軽率"],
 *   meaning_upright: "新しい始まり、純粋な冒険心...",
 *   meaning_reversed: "無謀な行動、準備不足..."
 * }
 *
 * SPREADS_DATA の各要素フォーマット想定:
 * {
 *   id: "celtic_cross",
 *   name: "ケルティッククロス",
 *   positions: [
 *     { id: "p1", label: "現在の状況" },
 *     { id: "p2", label: "障害・課題" },
 *     ...
 *   ]
 * }
 */

'use strict';

// ─────────────────────────────────────────────
// 0. グローバル状態
// ─────────────────────────────────────────────
/** @type {Array<{positionId: string, card: Object, isReversed: boolean, note: string}>} */
let currentDrawResult = [];

/** @type {SpeechRecognition|null} 現在アクティブな音声認識インスタンス */
let activeRecognition = null;

/** @type {string|null} 現在録音中のポジションID */
let recordingPositionId = null;

/** @type {Array<Object>} 現在選択されているスプレッドのポジション配列 */
let currentPositions = [];

/** @type {Array<Object>} スプレッド定義一覧（SPREADS_DATA） */
let spreadsData = [];

// ─────────────────────────────────────────────
// 1. 初期化
// ─────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
  await loadSpreadsData();
  initSpreadSelector();
  initDrawButton();
  initGenerateButton();
  initFormatRadio();
});

/**
 * spreads.json を fetch して spreadsData に格納する。
 * グローバル変数 SPREADS_DATA が既に存在する場合はそちらを優先する。
 */
async function loadSpreadsData() {
  // cards_data.js 側で SPREADS_DATA がグローバル注入済みの場合
  if (typeof SPREADS_DATA !== 'undefined' && Array.isArray(SPREADS_DATA)) {
    spreadsData = SPREADS_DATA;
    return;
  }

  try {
    const response = await fetch('registry/spreads.json');
    if (!response.ok) {
      throw new Error(`spreads.json の取得に失敗: ${response.status}`);
    }
    spreadsData = await response.json();
  } catch (err) {
    console.error('スプレッドデータの読み込みエラー:', err);
    // フォールバック: 最低限のスプレッドをハードコード
    spreadsData = [
      {
        id: 'one_card',
        name: '1枚引き',
        positions: [
          { id: 'p1', label: '現在のメッセージ' }
        ]
      },
      {
        id: 'three_card',
        name: '3枚引き（過去・現在・未来）',
        positions: [
          { id: 'p1', label: '過去' },
          { id: 'p2', label: '現在' },
          { id: 'p3', label: '未来' }
        ]
      },
      {
        id: 'celtic_cross',
        name: 'ケルティッククロス（10枚）',
        positions: [
          { id: 'p1',  label: '現在の状況' },
          { id: 'p2',  label: '障害・課題' },
          { id: 'p3',  label: '遠い過去' },
          { id: 'p4',  label: '近い過去' },
          { id: 'p5',  label: '可能性・目標' },
          { id: 'p6',  label: '近い未来' },
          { id: 'p7',  label: '自分自身' },
          { id: 'p8',  label: '周囲の影響' },
          { id: 'p9',  label: '希望と恐れ' },
          { id: 'p10', label: '最終結果' }
        ]
      }
    ];
  }
}

// ─────────────────────────────────────────────
// 2. スプレッド選択セレクトボックス
// ─────────────────────────────────────────────
function initSpreadSelector() {
  const selector = document.getElementById('spread-selector');
  if (!selector) {
    console.error('#spread-selector が見つかりません');
    return;
  }

  // セレクトボックスの選択肢を動的生成
  selector.innerHTML = '';
  spreadsData.forEach((spread) => {
    const option = document.createElement('option');
    option.value = spread.id;
    option.textContent = spread.name;
    selector.appendChild(option);
  });

  // 初期表示
  renderSpreadContainer(selector.value);

  // 変更イベント
  selector.addEventListener('change', (e) => {
    stopActiveRecognition();
    currentDrawResult = [];
    renderSpreadContainer(e.target.value);
  });
}

/**
 * 指定スプレッドIDに対応するカード枠を #spread-container に描画する。
 * @param {string} spreadId
 */
function renderSpreadContainer(spreadId) {
  const spread = spreadsData.find((s) => s.id === spreadId);
  if (!spread) {
    console.error(`スプレッド "${spreadId}" が見つかりません`);
    return;
  }

  currentPositions = spread.positions;

  const container = document.getElementById('spread-container');
  if (!container) {
    console.error('#spread-container が見つかりません');
    return;
  }

  container.innerHTML = '';

  spread.positions.forEach((pos) => {
    const posEl = createPositionElement(pos);
    container.appendChild(posEl);
  });
}

/**
 * 1ポジション分のHTML要素を生成して返す。
 * @param {{ id: string, label: string }} pos
 * @returns {HTMLElement}
 */
function createPositionElement(pos) {
  const wrapper = document.createElement('div');
  wrapper.className = 'position-card';
  wrapper.id = `pos-${pos.id}`;
  wrapper.dataset.positionId = pos.id;

  // ── ヘッダー（ポジション名） ──
  const header = document.createElement('div');
  header.className = 'position-header';
  header.textContent = pos.label;
  wrapper.appendChild(header);

  // ── カード情報エリア（カードを引くまでは空） ──
  const cardInfo = document.createElement('div');
  cardInfo.className = 'card-info';
  cardInfo.id = `card-info-${pos.id}`;
  cardInfo.textContent = '— カード未選択 —';
  wrapper.appendChild(cardInfo);

  // ── 鑑定メモ ラベル ──
  const noteLabel = document.createElement('label');
  noteLabel.className = 'note-label';
  noteLabel.textContent = '鑑定メモ（手動入力 or 音声）:';
  noteLabel.setAttribute('for', `note-${pos.id}`);
  wrapper.appendChild(noteLabel);

  // ── テキストエリア（鑑定メモ） ──
  const textarea = document.createElement('textarea');
  textarea.className = 'note-textarea';
  textarea.id = `note-${pos.id}`;
  textarea.dataset.positionId = pos.id;
  textarea.placeholder = 'ここに鑑定メモを入力、または下のボタンで音声入力...';
  textarea.rows = 4;
  wrapper.appendChild(textarea);

  // ── 音声ボタンエリア ──
  const voiceArea = document.createElement('div');
  voiceArea.className = 'voice-area';

  const startBtn = document.createElement('button');
  startBtn.className = 'voice-btn voice-start-btn';
  startBtn.id = `voice-start-${pos.id}`;
  startBtn.dataset.positionId = pos.id;
  startBtn.textContent = '🎤 録音開始';
  startBtn.addEventListener('click', () => onVoiceStart(pos.id));

  const stopBtn = document.createElement('button');
  stopBtn.className = 'voice-btn voice-stop-btn';
  stopBtn.id = `voice-stop-${pos.id}`;
  stopBtn.dataset.positionId = pos.id;
  stopBtn.textContent = '🛑 停止';
  stopBtn.disabled = true;
  stopBtn.addEventListener('click', () => onVoiceStop(pos.id));

  voiceArea.appendChild(startBtn);
  voiceArea.appendChild(stopBtn);
  wrapper.appendChild(voiceArea);

  // ── 録音状態表示ラベル ──
  const statusLabel = document.createElement('span');
  statusLabel.className = 'recording-status';
  statusLabel.id = `recording-status-${pos.id}`;
  statusLabel.textContent = '';
  wrapper.appendChild(statusLabel);

  return wrapper;
}

// ─────────────────────────────────────────────
// 3. カードを引く（ドローボタン）
// ─────────────────────────────────────────────
function initDrawButton() {
  const btn = document.getElementById('draw-btn');
  if (!btn) {
    console.error('#draw-btn が見つかりません');
    return;
  }
  btn.addEventListener('click', onDrawCards);
}

/**
 * カードを引く処理。
 * TAROT_DATA から currentPositions の枚数分、重複なしでランダム選択し、
 * 正逆もランダムに決定して各ポジションのカード情報エリアに描画する。
 */
function onDrawCards() {
  // TAROT_DATA の存在確認
  if (typeof TAROT_DATA === 'undefined' || !Array.isArray(TAROT_DATA) || TAROT_DATA.length === 0) {
    alert('TAROT_DATA が読み込まれていません。js/cards_data.js を確認してください。');
    return;
  }

  if (currentPositions.length === 0) {
    alert('スプレッドが選択されていません。');
    return;
  }

  const posCount = currentPositions.length;
  if (posCount > TAROT_DATA.length) {
    alert(`カード枚数(${TAROT_DATA.length})より多いポジション数(${posCount})は引けません。`);
    return;
  }

  // シャッフル（Fisher-Yates アルゴリズム）して先頭 posCount 枚を取得
  const shuffled = fisherYatesShuffle([...TAROT_DATA]);
  const drawn = shuffled.slice(0, posCount);

  // 結果を currentDrawResult に格納し、UI に反映
  currentDrawResult = [];

  currentPositions.forEach((pos, index) => {
    const card = drawn[index];
    const isReversed = Math.random() < 0.5; // 50% で逆位置

    // 既存のメモを保持（再引きでもメモは消さない仕様。消したい場合は '' に変更）
    const existingTextarea = document.getElementById(`note-${pos.id}`);
    const existingNote = existingTextarea ? existingTextarea.value : '';

    currentDrawResult.push({
      positionId: pos.id,
      positionLabel: pos.label,
      card: card,
      isReversed: isReversed,
      note: existingNote
    });

    renderCardInfo(pos.id, pos.label, card, isReversed);
  });
}

/**
 * Fisher-Yates シャッフル（破壊的）
 * @param {Array} array
 * @returns {Array} シャッフルされた同一配列
 */
function fisherYatesShuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const temp = array[i];
    array[i] = array[j];
    array[j] = temp;
  }
  return array;
}

/**
 * 特定ポジションのカード情報エリアを更新する。
 * @param {string} positionId
 * @param {string} positionLabel
 * @param {Object} card - TAROT_DATA の1要素
 * @param {boolean} isReversed
 */
function renderCardInfo(positionId, positionLabel, card, isReversed) {
  const infoEl = document.getElementById(`card-info-${positionId}`);
  if (!infoEl) return;

  const orientation = isReversed ? '逆位置' : '正位置';
  const keywords = isReversed
    ? (card.keywords_reversed || []).join('・')
    : (card.keywords_upright || []).join('・');
  const meaning = isReversed
    ? (card.meaning_reversed || card.meaning_upright || '（意味データなし）')
    : (card.meaning_upright || '（意味データなし）');

  infoEl.innerHTML = '';

  // カード名 + 正逆
  const nameEl = document.createElement('div');
  nameEl.className = 'card-name';
  nameEl.textContent = `${card.name}（${orientation}）`;
  if (card.name_en) {
    const enEl = document.createElement('span');
    enEl.className = 'card-name-en';
    enEl.textContent = ` / ${card.name_en}`;
    nameEl.appendChild(enEl);
  }
  infoEl.appendChild(nameEl);

  // キーワード
  if (keywords) {
    const kwEl = document.createElement('div');
    kwEl.className = 'card-keywords';
    kwEl.textContent = `🔑 ${keywords}`;
    infoEl.appendChild(kwEl);
  }

  // 意味
  const meaningEl = document.createElement('div');
  meaningEl.className = 'card-meaning';
  meaningEl.textContent = meaning;
  infoEl.appendChild(meaningEl);

  // ポジションカード枠自体にアニメーションクラスを付与
  const posEl = document.getElementById(`pos-${positionId}`);
  if (posEl) {
    posEl.classList.add('card-drawn');
    // アニメーション終了後にクラス除去（繰り返し引けるように）
    posEl.addEventListener('animationend', () => {
      posEl.classList.remove('card-drawn');
    }, { once: true });
  }
}

// ─────────────────────────────────────────────
// 4. 音声認識（Web Speech API）
// ─────────────────────────────────────────────

/**
 * 特定ポジションの録音を開始する。
 * 他のポジションが録音中なら先に安全停止する。
 * @param {string} positionId
 */
function onVoiceStart(positionId) {
  // ブラウザサポート確認
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    alert(
      'このブラウザは Web Speech API に対応していません。\n' +
      'Google Chrome または Microsoft Edge をお使いください。'
    );
    return;
  }

  // 現在別のポジションが録音中なら安全に停止
  if (activeRecognition !== null) {
    stopActiveRecognition();
    // 停止には少し時間が必要な場合があるため、遅延して次の録音を開始
    setTimeout(() => {
      startRecognitionForPosition(positionId, SpeechRecognition);
    }, 300);
    return;
  }

  startRecognitionForPosition(positionId, SpeechRecognition);
}

/**
 * 指定ポジションの音声認識を実際に開始する内部関数。
 * @param {string} positionId
 * @param {typeof SpeechRecognition} SpeechRecognitionClass
 */
function startRecognitionForPosition(positionId, SpeechRecognitionClass) {
  const recognition = new SpeechRecognitionClass();
  recognition.lang = 'ja-JP';
  recognition.interimResults = true;  // 途中結果も取得
  recognition.maxAlternatives = 1;
  recognition.continuous = true;      // 自動で止まらないよう連続モード

  activeRecognition = recognition;
  recordingPositionId = positionId;

  // UI を録音中状態に変更
  setRecordingUI(positionId, true);

  // 途中結果のバッファ（interim text を管理）
  let interimBuffer = '';

  recognition.onresult = (event) => {
    const textarea = document.getElementById(`note-${positionId}`);
    if (!textarea) return;

    let finalText = '';
    interimBuffer = '';

    for (let i = event.resultIndex; i < event.results.length; i++) {
      const result = event.results[i];
      if (result.isFinal) {
        finalText += result[0].transcript;
      } else {
        interimBuffer += result[0].transcript;
      }
    }

    // 最終結果をテキストエリアに追記
    if (finalText) {
      textarea.value += finalText;
      // currentDrawResult のメモも同期
      syncNoteToDrawResult(positionId, textarea.value);
    }

    // 途中結果はステータスラベルにプレビュー表示
    const statusEl = document.getElementById(`recording-status-${positionId}`);
    if (statusEl && interimBuffer) {
      statusEl.textContent = `📝 認識中: ${interimBuffer}`;
    }
  };

  recognition.onerror = (event) => {
    console.error(`音声認識エラー (${positionId}):`, event.error);

    let errorMsg = '音声認識エラーが発生しました。';
    switch (event.error) {
      case 'no-speech':
        errorMsg = '音声が検出されませんでした。もう一度お試しください。';
        break;
      case 'audio-capture':
        errorMsg = 'マイクが見つかりません。マイクの接続を確認してください。';
        break;
      case 'not-allowed':
        errorMsg = 'マイクへのアクセスが拒否されました。ブラウザの設定を確認してください。';
        break;
      case 'network':
        errorMsg = 'ネットワークエラーが発生しました。接続を確認してください。';
        break;
      case 'aborted':
        // 意図的な停止なので通知不要
        errorMsg = '';
        break;
    }

    if (errorMsg) {
      const statusEl = document.getElementById(`recording-status-${positionId}`);
      if (statusEl) {
        statusEl.textContent = `⚠️ ${errorMsg}`;
        statusEl.style.color = 'var(--color-error, #e53e3e)';
      }
    }

    cleanupRecognitionState(positionId);
  };

  recognition.onend = () => {
    // continuous=true でも何らかの理由で終了した場合の後処理
    if (recordingPositionId === positionId) {
      cleanupRecognitionState(positionId);
    }
  };

  recognition.onstart = () => {
    const statusEl = document.getElementById(`recording-status-${positionId}`);
    if (statusEl) {
      statusEl.textContent = '🔴 録音中...';
      statusEl.style.color = 'var(--color-recording, #e53e3e)';
    }
  };

  try {
    recognition.start();
  } catch (err) {
    console.error('recognition.start() 失敗:', err);
    cleanupRecognitionState(positionId);
  }
}

/**
 * 特定ポジションの録音を停止する（ボタン押下時）。
 * @param {string} positionId
 */
function onVoiceStop(positionId) {
  if (recordingPositionId !== positionId) return;
  stopActiveRecognition();
}

/**
 * 現在アクティブな音声認識を安全に停止する。
 */
function stopActiveRecognition() {
  if (activeRecognition) {
    try {
      activeRecognition.stop();
    } catch (err) {
      console.warn('activeRecognition.stop() 失敗（既に停止済みの可能性）:', err);
    }
    // onend が呼ばれるが、念のため即時クリーンアップ
    if (recordingPositionId) {
      cleanupRecognitionState(recordingPositionId);
    }
    activeRecognition = null;
    recordingPositionId = null;
  }
}

/**
 * 録音終了後の状態クリーンアップ（UI リセット + 内部状態リセット）。
 * @param {string} positionId
 */
function cleanupRecognitionState(positionId) {
  setRecordingUI(positionId, false);

  const statusEl = document.getElementById(`recording-status-${positionId}`);
  if (statusEl && statusEl.textContent.startsWith('🔴')) {
    statusEl.textContent = '✅ 録音停止';
    statusEl.style.color = 'var(--color-success, #38a169)';
    // 3秒後にステータスをクリア
    setTimeout(() => {
      if (statusEl) {
        statusEl.textContent = '';
        statusEl.style.color = '';
      }
    }, 3000);
  }

  if (recordingPositionId === positionId) {
    activeRecognition = null;
    recordingPositionId = null;
  }
}

/**
 * 指定ポジションの録音関連 UI を録音中 or 停止中に切り替える。
 * @param {string} positionId
 * @param {boolean} isRecording
 */
function setRecordingUI(positionId, isRecording) {
  const startBtn = document.getElementById(`voice-start-${positionId}`);
  const stopBtn  = document.getElementById(`voice-stop-${positionId}`);
  const posEl    = document.getElementById(`pos-${positionId}`);

  if (startBtn) {
    startBtn.disabled = isRecording;
    startBtn.textContent = isRecording ? '🎙️ 録音中...' : '🎤 録音開始';
  }
  if (stopBtn) {
    stopBtn.disabled = !isRecording;
  }
  if (posEl) {
    if (isRecording) {
      posEl.classList.add('recording-active');
    } else {
      posEl.classList.remove('recording-active');
    }
  }
}

/**
 * テキストエリアの内容を currentDrawResult に同期する。
 * @param {string} positionId
 * @param {string} noteValue
 */
function syncNoteToDrawResult(positionId, noteValue) {
  const entry = currentDrawResult.find((r) => r.positionId === positionId);
  if (entry) {
    entry.note = noteValue;
  }
}

// ─────────────────────────────────────────────
// 5. 出力フォーマット（Markdown / JSON）ラジオボタン
// ─────────────────────────────────────────────
function initFormatRadio() {
  const radios = document.querySelectorAll('input[name="output-format"]');
  radios.forEach((radio) => {
    radio.addEventListener('change', () => {
      // フォーマット変更時に出力エリアをクリア（古い形式の出力が残らないように）
      const outputTextarea = document.getElementById('output-textarea');
      if (outputTextarea) {
        outputTextarea.value = '';
      }
    });
  });
}

/**
 * 現在選択されている出力フォーマットを返す。
 * @returns {'markdown'|'json'}
 */
function getSelectedFormat() {
  const selectedRadio = document.querySelector('input[name="output-format"]:checked');
  if (!selectedRadio) return 'markdown';
  return selectedRadio.value === 'json' ? 'json' : 'markdown';
}

// ─────────────────────────────────────────────
// 6. 鑑定結果を生成
// ─────────────────────────────────────────────
function initGenerateButton() {
  const btn = document.getElementById('generate-btn');
  if (!btn) {
    console.error('#generate-btn が見つかりません');
    return;
  }
  btn.addEventListener('click', onGenerateResult);
}

/**
 * 「鑑定結果を生成」ボタン押下時の処理。
 * 各ポジションのテキストエリアからメモを最新取得し、
 * Markdown または JSON 形式で #output-textarea に出力する。
 */
function onGenerateResult() {
  if (currentPositions.length === 0) {
    alert('スプレッドが選択されていません。');
    return;
  }

  if (currentDrawResult.length === 0) {
    alert('先にカードを引いてください（「カードを引く」ボタンを押してください）。');
    return;
  }

  // 現在のテキストエリアの内容を currentDrawResult に同期
  currentDrawResult.forEach((entry) => {
    const textarea = document.getElementById(`note-${entry.positionId}`);
    if (textarea) {
      entry.note = textarea.value;
    }
  });

  const format = getSelectedFormat();
  let outputText = '';

  if (format === 'json') {
    outputText = generateJsonOutput();
  } else {
    outputText = generateMarkdownOutput();
  }

  const outputTextarea = document.getElementById('output-textarea');
  if (outputTextarea) {
    outputTextarea.value = outputText;
    // 生成後にスクロール
    outputTextarea.scrollTop = 0;
  }
}

/**
 * Markdown 形式で鑑定結果テキストを生成して返す。
 * @returns {string}
 */
function generateMarkdownOutput() {
  const lines = [];
  const now = new Date();
  const dateStr = `${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日 ` +
                  `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;

  // スプレッド名を取得
  const selector = document.getElementById('spread-selector');
  const spreadName = selector ? selector.options[selector.selectedIndex]?.text ?? 'タロット鑑定' : 'タロット鑑定';

  lines.push(`# タロット鑑定結果`);
  lines.push('');
  lines.push(`**スプレッド:** ${spreadName}`);
  lines.push(`**日時:** ${dateStr}`);
  lines.push('');
  lines.push('---');
  lines.push('');

  // 各ポジションをループ
  currentDrawResult.forEach((entry, index) => {
    const orientation = entry.isReversed ? '逆位置' : '正位置';
    const cardName    = entry.card.name ?? '（不明）';
    const cardNameEn  = entry.card.name_en ? ` / ${entry.card.name_en}` : '';
    const keywords    = entry.isReversed
      ? (entry.card.keywords_reversed ?? []).join('・')
      : (entry.card.keywords_upright  ?? []).join('・');
    const meaning     = entry.isReversed
      ? (entry.card.meaning_reversed ?? entry.card.meaning_upright ?? '')
      : (entry.card.meaning_upright  ?? '');
    const note        = entry.note ? entry.note.trim() : '';

    lines.push(`## ${index + 1}. 【${entry.positionLabel}】`);
    lines.push('');
    lines.push(`### ${cardName}${cardNameEn}（${orientation}）`);
    lines.push('');

    if (keywords) {
      lines.push(`**キーワード:** ${keywords}`);
      lines.push('');
    }

    if (meaning) {
      lines.push(`**基本の意味:**`);
      lines.push('');
      lines.push(meaning);
      lines.push('');
    }

    if (note) {
      lines.push(`**鑑定メモ:**`);
      lines.push('');
      lines.push(note);
      lines.push('');
    }

    lines.push('---');
    lines.push('');
  });

  lines.push('*（このテキストはタロット鑑定アプリによって自動生成されました）*');

  return lines.join('\n');
}

/**
 * JSON 形式で鑑定結果テキストを生成して返す。
 * @returns {string}
 */
function generateJsonOutput() {
  const now = new Date();
  const selector = document.getElementById('spread-selector');
  const spreadId   = selector ? selector.value : '';
  const spreadName = selector ? (selector.options[selector.selectedIndex]?.text ?? '') : '';

  const resultObj = {
    generated_at: now.toISOString(),
    spread_id: spreadId,
    spread_name: spreadName,
    positions: currentDrawResult.map((entry) => {
      const orientation = entry.isReversed ? 'reversed' : 'upright';
      const keywords    = entry.isReversed
        ? (entry.card.keywords_reversed ?? [])
        : (entry.card.keywords_upright  ?? []);
      const meaning     = entry.isReversed
        ? (entry.card.meaning_reversed ?? entry.card.meaning_upright ?? '')
        : (entry.card.meaning_upright  ?? '');

      return {
        position_id:    entry.positionId,
        position_label: entry.positionLabel,
        card: {
          id:          entry.card.id,
          name:        entry.card.name,
          name_en:     entry.card.name_en ?? '',
          orientation: orientation,
          keywords:    keywords,
          meaning:     meaning
        },
        user_note: entry.note ? entry.note.trim() : ''
      };
    })
  };

  return JSON.stringify(resultObj, null, 2);
}

// ─────────────────────────────────────────────
// 7. ユーティリティ: ページ離脱時に録音を安全停止
// ─────────────────────────────────────────────
window.addEventListener('beforeunload', () => {
  stopActiveRecognition();
});

// ─────────────────────────────────────────────
// 8. テキストエリア変更時に drawResult に同期
//    （手動入力にも対応するため、input イベントで追跡）
// ─────────────────────────────────────────────
document.addEventListener('input', (e) => {
  const el = e.target;
  if (el.classList.contains('note-textarea') && el.dataset.positionId) {
    syncNoteToDrawResult(el.dataset.positionId, el.value);
  }
});
