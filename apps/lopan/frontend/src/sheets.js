// Google Sheets 連携用ユーティリティ
// 必要に応じて fetch でGAS Web APIやバックエンド経由でスプレッドシートに書き込む

export async function saveToSpreadsheet({ angle, directionInfo, userInput }) {
  // TODO: Google Apps Script Web APIエンドポイント or Flask経由APIを指定
  const endpoint = process.env.REACT_APP_SHEET_API_URL || 'https://script.google.com/macros/s/xxxx/exec';
  const payload = {
    angle,
    directionInfo,
    userInput,
    timestamp: new Date().toISOString(),
  };
  try {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('スプレッドシート送信失敗');
    return await res.json();
  } catch (e) {
    throw e;
  }
}
