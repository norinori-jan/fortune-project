/**
 * reading_engine.js — タロット鑑定エンジン 強化版
 * fortune-project 用
 *
 * 機能:
 *   - カードの意味をポジション文脈で深く解釈
 *   - 複数カード間の関係性分析（エレメント、数値、スート）
 *   - AI 連携用プロンプトの自動構築
 *   - 鑑定レポートの構造化出力
 *   - カード間の相性スコアリング
 *
 * 依存:
 *   - TAROT_DATA (グローバル or モジュールインポート)
 */

'use strict';

// ─────────────────────────────────────────────
// 0. エレメント・数秘術メタデータ
//    (大アルカナ22枚に対応)
// ─────────────────────────────────────────────

/**
 * カードIDに対するエレメント（元素）マッピング。
 * 大アルカナは火・水・風・土・エーテルに分類。
 */
const CARD_ELEMENTS = {
  0:  'air',    // 愚者
  1:  'air',    // 魔術師
  2:  'water',  // 女教皇
  3:  'earth',  // 女帝
  4:  'fire',   // 皇帝
  5:  'earth',  // 法王
  6:  'air',    // 恋人
  7:  'water',  // 戦車
  8:  'fire',   // 力
  9:  'earth',  // 隠者
  10: 'fire',   // 運命の輪
  11: 'air',    // 正義
  12: 'water',  // 吊られた男
  13: 'water',  // 死神
  14: 'fire',   // 節制
  15: 'earth',  // 悪魔
  16: 'fire',   // 塔
  17: 'air',    // 星
  18: 'water',  // 月
  19: 'fire',   // 太陽
  20: 'fire',   // 審判
  21: 'earth',  // 世界
};

/**
 * エレメント間の相性スコア。
 * 1.0 = 中立, 1.5 = 相性良好, 0.5 = 相性困難
 */
const ELEMENT_AFFINITY = {
  fire:  { fire: 1.0, air:  1.5, water: 0.5, earth: 0.5 },
  water: { fire: 0.5, air:  0.5, water: 1.0, earth: 1.5 },
  air:   { fire: 1.5, air:  1.0, water: 0.5, earth: 0.5 },
  earth: { fire: 0.5, air:  0.5, water: 1.5, earth: 1.0 },
};

/**
 * カードIDに対応する数秘術的数値（大アルカナの番号をそのまま使用）。
 * @param {number} cardId
 * @returns {number}
 */
function getNumerologicalNumber(cardId) {
  // 愚者(0)は22として扱う（完成の数）
  return cardId === 0 ? 22 : cardId;
}

// ─────────────────────────────────────────────
// 1. 鑑定エンジン本体クラス
// ─────────────────────────────────────────────

class TarotReadingEngine {
  /**
   * @param {Array<Object>} tarotData - TAROT_DATA 配列
   */
  constructor(tarotData) {
    if (!Array.isArray(tarotData) || tarotData.length === 0) {
      throw new Error('TarotReadingEngine: tarotData が空か無効です。');
    }
    this.tarotData = tarotData;
  }

  // ─────────────────────────────────────
  // 1-1. カードを引く（重複なし、正逆ランダム）
  // ─────────────────────────────────────

  /**
   * 指定枚数のカードをシャッフルして引く。
   * @param {number} count - 引く枚数
   * @returns {Array<{card: Object, isReversed: boolean}>}
   */
  drawCards(count) {
    if (count > this.tarotData.length) {
      throw new Error(`引く枚数(${count})がカード総数(${this.tarotData.length})を超えています。`);
    }

    const shuffled = this._fisherYatesShuffle([...this.tarotData]);
    const drawn = shuffled.slice(0, count);

    return drawn.map((card) => ({
      card,
      isReversed: Math.random() < 0.5
    }));
  }

  /**
   * Fisher-Yates シャッフル（破壊的）。
   * @param {Array} array
   * @returns {Array}
   */
  _fisherYatesShuffle(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const temp = array[i];
      array[i] = array[j];
      array[j] = temp;
    }
    return array;
  }

  // ─────────────────────────────────────
  // 1-2. 単一カードの解釈生成
  // ─────────────────────────────────────

  /**
   * 単一カードのポジション文脈に基づいた解釈テキストを生成する。
   * @param {Object} card - TAROT_DATA の1要素
   * @param {boolean} isReversed
   * @param {string} positionLabel - ポジション名（例: "現在の状況"）
   * @param {string} [userNote=''] - ユーザーの鑑定メモ
   * @returns {string} 解釈テキスト
   */
  interpretCard(card, isReversed, positionLabel, userNote = '') {
    const orientation = isReversed ? '逆位置' : '正位置';
    const keywords = isReversed
      ? (card.keywords_reversed ?? []).join('、')
      : (card.keywords_upright  ?? []).join('、');
    const meaning = isReversed
      ? (card.meaning_reversed ?? card.meaning_upright ?? '')
      : (card.meaning_upright  ?? '');

    let interpretation = `【${positionLabel}】${card.name}（${orientation}）\n`;

    if (keywords) {
      interpretation += `キーワード: ${keywords}\n`;
    }

    if (meaning) {
      interpretation += `意味: ${meaning}\n`;
    }

    // ポジションラベルによる文脈的コメントを追加
    const contextComment = this._generatePositionContext(positionLabel, card, isReversed);
    if (contextComment) {
      interpretation += `文脈的解釈: ${contextComment}\n`;
    }

    if (userNote && userNote.trim()) {
      interpretation += `鑑定師のメモ: ${userNote.trim()}\n`;
    }

    return interpretation;
  }

  /**
   * ポジションのラベルとカードの組み合わせによる文脈コメントを生成する。
   * @param {string} positionLabel
   * @param {Object} card
   * @param {boolean} isReversed
   * @returns {string}
   */
  _generatePositionContext(positionLabel, card, isReversed) {
    const label = positionLabel.toLowerCase();
    const cardName = card.name;

    // 過去ポジション
    if (label.includes('過去') || label.includes('past')) {
      return isReversed
        ? `過去において、${cardName}の逆位置エネルギーがあなたの経験に影を落としていた可能性があります。`
        : `過去に${cardName}のポジティブなエネルギーがあなたの基盤を形成しました。`;
    }

    // 現在ポジション
    if (label.includes('現在') || label.includes('present') || label.includes('状況')) {
      return isReversed
        ? `現在、${cardName}の逆位置は内的なブロックや未解決の課題を示しています。`
        : `現在、${cardName}のエネルギーがあなたの状況に直接影響を与えています。`;
    }

    // 未来ポジション
    if (label.includes('未来') || label.includes('future') || label.includes('結果')) {
      return isReversed
        ? `${cardName}の逆位置は、注意を払わなければ起こりうる困難な展開を示唆します。`
        : `${cardName}は前向きな未来の可能性を指し示しています。`;
    }

    // 障害・課題ポジション
    if (label.includes('障害') || label.includes('課題') || label.includes('challenge')) {
      return isReversed
        ? `${cardName}の逆位置が示す障害は、内面的な抵抗から生じているかもしれません。`
        : `${cardName}はあなたが乗り越えるべき外的な課題を象徴しています。`;
    }

    // アドバイスポジション
    if (label.includes('アドバイス') || label.includes('advice') || label.includes('助言')) {
      return isReversed
        ? `${cardName}の逆位置からのアドバイス: 今は慎重に、内省を深めてください。`
        : `${cardName}からのアドバイス: そのエネルギーを積極的に活用してください。`;
    }

    // 一般的なコメント
    return '';
  }

  // ─────────────────────────────────────
  // 1-3. カード間の関係性分析
  // ─────────────────────────────────────

  /**
   * ドロー結果の全カード間の関係性を分析する。
   * @param {Array<{card: Object, isReversed: boolean}>} drawnCards
   * @returns {Object} 分析結果
   */
  analyzeCardRelationships(drawnCards) {
    if (!drawnCards || drawnCards.length === 0) {
      return { summary: 'カードが引かれていません。', details: [] };
    }

    const details = [];
    let overallAffinityScore = 0;
    let pairCount = 0;

    // エレメント集計
    const elementCounts = { fire: 0, water: 0, air: 0, earth: 0 };
    drawnCards.forEach(({ card }) => {
      const element = CARD_ELEMENTS[card.id] ?? 'air';
      elementCounts[element]++;
    });

    // 逆位置の割合
    const reversedCount = drawnCards.filter((c) => c.isReversed).length;
    const reversedRatio  = (reversedCount / drawnCards.length) * 100;

    // 隣接カードペアの相性スコアを計算
    for (let i = 0; i < drawnCards.length - 1; i++) {
      const cardA    = drawnCards[i].card;
      const cardB    = drawnCards[i + 1].card;
      const elemA    = CARD_ELEMENTS[cardA.id] ?? 'air';
      const elemB    = CARD_ELEMENTS[cardB.id] ?? 'air';
      const affinity = ELEMENT_AFFINITY[elemA]?.[elemB] ?? 1.0;

      overallAffinityScore += affinity;
      pairCount++;

      if (affinity > 1.0) {
        details.push(`${cardA.name} と ${cardB.name} はエレメント的に相性が良い組み合わせです（${elemA} × ${elemB}）。`);
      } else if (affinity < 1.0) {
        details.push(`${cardA.name} と ${cardB.name} はエレメント的に緊張関係にあります（${elemA} × ${elemB}）。これは変容のエネルギーを示す場合があります。`);
      }
    }

    const avgAffinity = pairCount > 0 ? overallAffinityScore / pairCount : 1.0;

    // 支配的エレメントを特定
    const dominantElement = Object.entries(elementCounts)
      .sort(([, a], [, b]) => b - a)[0][0];

    const dominantElementMap = {
      fire:  '火（情熱・行動・変革）',
      water: '水（感情・直感・関係）',
      air:   '風（知性・コミュニケーション・変化）',
      earth: '土（安定・物質・実務）'
    };

    // 数秘術的合計
    const numSum = drawnCards.reduce((sum, { card }) => {
      return sum + getNumerologicalNumber(card.id);
    }, 0);
    const reducedNum = this._reduceToSingleDigit(numSum);

    // サマリー生成
    let summary = '';
    summary += `引かれた${drawnCards.length}枚のカードから見えるエネルギー:\n`;
    summary += `支配的エレメント: ${dominantElementMap[dominantElement] ?? dominantElement}\n`;
    summary += `逆位置の割合: ${reversedRatio.toFixed(0)}%（${reversedCount}/${drawnCards.length}枚）\n`;
    summary += `カード間の調和スコア: ${(avgAffinity * 100).toFixed(0)}点/150点\n`;
    summary += `数秘術的総計: ${numSum} → ${reducedNum}\n`;

    if (reversedRatio > 60) {
      summary += '逆位置が多く、内省や変革が求められる時期を示しています。\n';
    } else if (reversedRatio < 20) {
      summary += 'ほとんどが正位置で、エネルギーが外向きに流れやすい状況です。\n';
    }

    return {
      summary,
      details,
      elementCounts,
      dominantElement,
      reversedRatio,
      averageAffinity: avgAffinity,
      numerologicalSum: numSum,
      reducedNumber: reducedNum
    };
  }

  /**
   * 数値を1桁に還元する（数秘術的還元）。
   * @param {number} n
   * @returns {number}
   */
  _reduceToSingleDigit(n) {
    while (n > 22) {
      n = String(n).split('').reduce((s, d) => s + parseInt(d, 10), 0);
    }
    return n;
  }

  // ─────────────────────────────────────
  // 1-4. AI 連携用プロンプトの自動構築
  // ─────────────────────────────────────

  /**
   * Anthropic API / OpenAI API に送信するためのプロンプトを自動生成する。
   * @param {Array<{positionLabel: string, card: Object, isReversed: boolean, note: string}>} readingData
   * @param {string} [spreadName=''] - スプレッド名
   * @param {string} [userQuestion=''] - 相談者の質問（任意）
   * @returns {string} プロンプト文字列
   */
  buildAIPrompt(readingData, spreadName = '', userQuestion = '') {
    const lines = [];

    lines.push('あなたはプロのタロット鑑定師です。以下のタロットカードの展開を深く読み解き、');
    lines.push('具体的で実践的な鑑定結果を日本語でお伝えください。');
    lines.push('');

    if (spreadName) {
      lines.push(`【スプレッド】${spreadName}`);
      lines.push('');
    }

    if (userQuestion && userQuestion.trim()) {
      lines.push(`【相談者の質問】${userQuestion.trim()}`);
      lines.push('');
    }

    lines.push('【展開されたカード】');
    lines.push('');

    readingData.forEach((entry, index) => {
      const orientation = entry.isReversed ? '逆位置' : '正位置';
      const keywords = entry.isReversed
        ? (entry.card.keywords_reversed ?? []).join('・')
        : (entry.card.keywords_upright  ?? []).join('・');
      const meaning = entry.isReversed
        ? (entry.card.meaning_reversed ?? entry.card.meaning_upright ?? '')
        : (entry.card.meaning_upright  ?? '');

      lines.push(`${index + 1}. 【${entry.positionLabel}】`);
      lines.push(`   カード: ${entry.card.name}（${orientation}）`);
      if (entry.card.name_en) {
        lines.push(`   英名: ${entry.card.name_en}`);
      }
      if (keywords) {
        lines.push(`   キーワード: ${keywords}`);
      }
      if (meaning) {
        lines.push(`   意味: ${meaning}`);
      }
      if (entry.note && entry.note.trim()) {
        lines.push(`   鑑定師メモ: ${entry.note.trim()}`);
      }
      lines.push('');
    });

    lines.push('【鑑定依頼】');
    lines.push('上記のカード展開を総合的に読み解き、以下の点をカバーした鑑定を行ってください:');
    lines.push('1. 各カードがそのポジションで示している具体的なメッセージ');
    lines.push('2. カード全体の流れやストーリー');
    lines.push('3. 相談者へのアドバイスと今後の見通し');
    lines.push('4. 特に注意すべき点や転換点');
    lines.push('');
    lines.push('鑑定は温かく、希望を持てるものにしてください。ただし、困難なカードも正直に伝えてください。');

    return lines.join('\n');
  }

  // ─────────────────────────────────────
  // 1-5. 完全鑑定レポートの生成
  // ─────────────────────────────────────

  /**
   * 完全な鑑定レポートを構造化オブジェクトとして生成する。
   * @param {Array<{positionLabel: string, positionId: string, card: Object, isReversed: boolean, note: string}>} readingData
   * @param {string} [spreadName='']
   * @param {string} [userQuestion='']
   * @returns {Object} レポートオブジェクト
   */
  generateFullReport(readingData, spreadName = '', userQuestion = '') {
    const now = new Date();

    // 個別カード解釈
    const cardInterpretations = readingData.map((entry) => ({
      positionId:    entry.positionId,
      positionLabel: entry.positionLabel,
      cardName:      entry.card.name,
      cardNameEn:    entry.card.name_en ?? '',
      orientation:   entry.isReversed ? 'reversed' : 'upright',
      keywords: entry.isReversed
        ? (entry.card.keywords_reversed ?? [])
        : (entry.card.keywords_upright  ?? []),
      meaning: entry.isReversed
        ? (entry.card.meaning_reversed ?? entry.card.meaning_upright ?? '')
        : (entry.card.meaning_upright  ?? ''),
      element:        CARD_ELEMENTS[entry.card.id] ?? 'unknown',
      numerology:     getNumerologicalNumber(entry.card.id),
      interpretation: this.interpretCard(entry.card, entry.isReversed, entry.positionLabel, entry.note),
      userNote:       entry.note ?? ''
    }));

    // カード間関係性分析
    const relationships = this.analyzeCardRelationships(
      readingData.map((e) => ({ card: e.card, isReversed: e.isReversed }))
    );

    // AI プロンプト
    const aiPrompt = this.buildAIPrompt(readingData, spreadName, userQuestion);

    return {
      meta: {
        generated_at:  now.toISOString(),
        spread_name:   spreadName,
        user_question: userQuestion,
        card_count:    readingData.length
      },
      card_interpretations: cardInterpretations,
      relationship_analysis: relationships,
      ai_prompt: aiPrompt
    };
  }

  // ─────────────────────────────────────
  // 1-6. Markdown レポート文字列の生成
  // ─────────────────────────────────────

  /**
   * generateFullReport の結果を Markdown テキストとして整形する。
   * @param {Object} report - generateFullReport の返値
   * @returns {string}
   */
  reportToMarkdown(report) {
    const lines = [];
    const { meta, card_interpretations, relationship_analysis } = report;

    lines.push('# タロット鑑定レポート（強化版）');
    lines.push('');

    if (meta.spread_name) {
      lines.push(`**スプレッド:** ${meta.spread_name}`);
    }
    lines.push(`**生成日時:** ${new Date(meta.generated_at).toLocaleString('ja-JP')}`);
    lines.push(`**枚数:** ${meta.card_count}枚`);

    if (meta.user_question) {
      lines.push('');
      lines.push(`**ご相談の内容:**`);
      lines.push(`> ${meta.user_question}`);
    }

    lines.push('');
    lines.push('---');
    lines.push('');
    lines.push('## 📊 エネルギー分析');
    lines.push('');
    lines.push(relationship_analysis.summary);

    if (relationship_analysis.details.length > 0) {
      lines.push('');
      lines.push('**カード間の関係性:**');
      relationship_analysis.details.forEach((d) => {
        lines.push(`- ${d}`);
      });
    }

    lines.push('');
    lines.push('---');
    lines.push('');
    lines.push('## 🃏 各カードの読み解き');
    lines.push('');

    card_interpretations.forEach((ci, index) => {
      lines.push(`### ${index + 1}. 【${ci.positionLabel}】`);
      lines.push('');
      lines.push(`**${ci.cardName}**（${ci.orientation === 'reversed' ? '逆位置' : '正位置'}）${ci.cardNameEn ? ' / ' + ci.cardNameEn : ''}`);
      lines.push('');

      if (ci.keywords.length > 0) {
        lines.push(`🔑 **キーワード:** ${ci.keywords.join('・')}`);
        lines.push('');
      }

      if (ci.meaning) {
        lines.push(`📖 **意味:** ${ci.meaning}`);
        lines.push('');
      }

      if (ci.interpretation) {
        // interpretCard の出力から文脈的解釈部分だけを抽出
        const ctxMatch = ci.interpretation.match(/文脈的解釈: (.+)/);
        if (ctxMatch) {
          lines.push(`💡 **文脈的解釈:** ${ctxMatch[1]}`);
          lines.push('');
        }
      }

      if (ci.userNote) {
        lines.push(`📝 **鑑定メモ:** ${ci.userNote}`);
        lines.push('');
      }

      lines.push(`*エレメント: ${ci.element} ／ 数秘: ${ci.numerology}*`);
      lines.push('');
      lines.push('---');
      lines.push('');
    });

    lines.push('## 🤖 AI 鑑定用プロンプト');
    lines.push('');
    lines.push('```');
    lines.push(report.ai_prompt);
    lines.push('```');
    lines.push('');
    lines.push('---');
    lines.push('');
    lines.push('*このレポートは TarotReadingEngine（強化版）によって生成されました。*');

    return lines.join('\n');
  }

  // ─────────────────────────────────────
  // 1-7. JSON レポート文字列の生成
  // ─────────────────────────────────────

  /**
   * generateFullReport の結果を整形済み JSON 文字列として返す。
   * @param {Object} report
   * @returns {string}
   */
  reportToJSON(report) {
    return JSON.stringify(report, null, 2);
  }
}

// ─────────────────────────────────────────────
// 2. エクスポート（モジュール環境）& グローバル公開
// ─────────────────────────────────────────────
if (typeof module !== 'undefined' && module.exports) {
  // Node.js / CommonJS
  module.exports = {
    TarotReadingEngine,
    CARD_ELEMENTS,
    ELEMENT_AFFINITY,
    getNumerologicalNumber
  };
} else {
  // ブラウザグローバル
  window.TarotReadingEngine   = TarotReadingEngine;
  window.CARD_ELEMENTS        = CARD_ELEMENTS;
  window.ELEMENT_AFFINITY     = ELEMENT_AFFINITY;
  window.getNumerologicalNumber = getNumerologicalNumber;
}
