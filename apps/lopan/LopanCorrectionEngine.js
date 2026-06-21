// LopanCorrectionEngine.js
// 104分割羅盤の補正ロジック

class LopanCorrectionEngine {
  constructor() {
    this.CELL_WIDTH = 360.0 / 104;
    this.CORRECTIONS = {}; // 実行時に外部から設定
  }
  
  /**
   * 24山の補正値を取得
   */
  getMountainCorrection(mountainId) {
    const corrections = this.CORRECTIONS['mountain_24'] || [];
    return corrections.find(m => m.id === mountainId) || null;
  }
  
  /**
   * CVSから読み込んだセルデータ + 補正を応用して描画
   */
  getCorrectedAngle(layerType, layerId) {
    const corrections = this.CORRECTIONS[layerType] || [];
    const item = corrections.find(obj => obj.id === layerId);
    return item ? item.actual : null;
  }
  
  /**
   * SVG描画時に補正線を追加
   */
  drawCorrectionLines(svgElement, layerType = 'mountain_24', radiusOuter = 100, radiusInner = 90) {
    const corrections = this.CORRECTIONS[layerType] || [];
    
    corrections.forEach(obj => {
      if (Math.abs(obj.correction) > 0.05) { // 誤差が0.05度以上のみ表示
        const angle = (obj.actual * Math.PI) / 180;
        
        const x1 = radiusInner * Math.cos(angle);
        const y1 = radiusInner * Math.sin(angle);
        const x2 = radiusOuter * Math.cos(angle);
        const y2 = radiusOuter * Math.sin(angle);
        
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', x1);
        line.setAttribute('y1', y1);
        line.setAttribute('x2', x2);
        line.setAttribute('y2', y2);
        line.setAttribute('stroke', 'red');
        line.setAttribute('stroke-width', '1');
        line.setAttribute('stroke-dasharray', '2,2');
        line.setAttribute('class', 'correction-line');
        line.setAttribute('title', `ID:${obj.id} 補正: ${obj.correction > 0 ? '+' : ''}${obj.correction.toFixed(3)}°`);
        
        svgElement.appendChild(line);
      }
    });
  }
  
  /**
   * テーブル形式で補正情報を表示
   */
  generateCorrectionTable(layerType = 'mountain_24') {
    const corrections = this.CORRECTIONS[layerType] || [];
    let html = '<table border="1"><tr><th>ID</th><th>理想(°)</th><th>実装(°)</th><th>補正(°)</th></tr>';
    
    corrections.forEach(obj => {
      const corrStr = obj.correction > 0 ? '+' : '';
      html += `<tr><td>${obj.id}</td><td>${obj.ideal.toFixed(2)}</td><td>${obj.actual.toFixed(2)}</td><td>${corrStr}${obj.correction.toFixed(4)}</td></tr>`;
    });
    
    html += '</table>';
    return html;
  }
}

// 使用例
// const engine = new LopanCorrectionEngine();
// engine.CORRECTIONS = correctionMapFromJSON; // サーバーから読み込み
// engine.drawCorrectionLines(svgElement, 'mountain_24');
