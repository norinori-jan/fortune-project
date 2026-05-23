import PropTypes from 'prop-types';

/**
 * 一本の爻（こう）を描画するコンポーネント
 * @param {number} value - 1: 陽（実線）, 0: 陰（破線）
 * @param {boolean} isChanging - 変爻かどうか
 * @param {number} position - 爻の位置 (1-6)
 */
function Line({ value, isChanging, position }) {
  const lineNames = { 1: '初爻', 2: '二爻', 3: '三爻', 4: '四爻', 5: '五爻', 6: '上爻' };

  return (
    <div className={`line-container ${isChanging ? 'changing' : ''}`} title={`${lineNames[position]}: ${value === 1 ? '陽' : '陰'}${isChanging ? '（変爻）' : ''}`}>
      {value === 1 ? (
        <div className="line yang" />
      ) : (
        <div className="line yin">
          <div className="yin-left" />
          <div className="yin-gap" />
          <div className="yin-right" />
        </div>
      )}
      {isChanging && <span className="changing-marker">●</span>}
    </div>
  );
}

Line.propTypes = {
  value: PropTypes.number.isRequired,
  isChanging: PropTypes.bool,
  position: PropTypes.number.isRequired,
};

Line.defaultProps = {
  isChanging: false,
};

/**
 * 六十四卦の卦象（かしょう）を視覚的に描画するコンポーネント
 * @param {object} hexagram - 卦データ
 * @param {number} changingLine - 変爻の位置 (1-6, 0=なし)
 * @param {string} label - ラベル（例: 「本卦」「之卦」）
 */
function Hexagram({ hexagram, changingLine, label }) {
  if (!hexagram) return null;

  // lines 配列は [初爻, 二爻, ..., 上爻] の順なので、表示は逆順（上爻が上）
  const reversedLines = [...hexagram.lines].reverse();

  return (
    <div className="hexagram-card">
      {label && <div className="hexagram-label">{label}</div>}
      <div className="hexagram-symbol">
        {hexagram.upper_trigram?.symbol}
        {hexagram.lower_trigram?.symbol}
      </div>
      <div className="hexagram-lines">
        {reversedLines.map((lineValue, idx) => {
          // 表示インデックス 0 = 上爻(6)、5 = 初爻(1)
          const position = 6 - idx;
          return (
            <Line
              key={position}
              value={lineValue}
              isChanging={changingLine === position}
              position={position}
            />
          );
        })}
      </div>
      <div className="hexagram-info">
        <div className="hexagram-number">第{hexagram.number}卦</div>
        <div className="hexagram-name">{hexagram.name}</div>
        <div className="hexagram-reading">（{hexagram.reading}）</div>
        <div className="hexagram-trigrams">
          <span>上卦: {hexagram.upper_trigram?.name}（{hexagram.upper_trigram?.element}）</span>
          <span>下卦: {hexagram.lower_trigram?.name}（{hexagram.lower_trigram?.element}）</span>
        </div>
        <div className="hexagram-trigrams">
          <span>上卦の徳: {hexagram.upper_trigram?.attribute} / 家族象: {hexagram.upper_trigram?.family}</span>
          <span>下卦の徳: {hexagram.lower_trigram?.attribute} / 家族象: {hexagram.lower_trigram?.family}</span>
        </div>
        <div className="hexagram-meaning">{hexagram.meaning}</div>
      </div>
    </div>
  );
}

Hexagram.propTypes = {
  hexagram: PropTypes.shape({
    number: PropTypes.number,
    name: PropTypes.string,
    reading: PropTypes.string,
    meaning: PropTypes.string,
    description: PropTypes.string,
    lines: PropTypes.arrayOf(PropTypes.number),
    upper_trigram: PropTypes.shape({
      name: PropTypes.string,
      element: PropTypes.string,
      symbol: PropTypes.string,
      attribute: PropTypes.string,
      family: PropTypes.string,
    }),
    lower_trigram: PropTypes.shape({
      name: PropTypes.string,
      element: PropTypes.string,
      symbol: PropTypes.string,
      attribute: PropTypes.string,
      family: PropTypes.string,
    }),
  }),
  changingLine: PropTypes.number,
  label: PropTypes.string,
};

Hexagram.defaultProps = {
  changingLine: 0,
  label: '',
};

export default Hexagram;
