// api.js
const MOUNTAINS = ['子','癸','丑','艮','寅','甲','卯','乙','辰','巽','巳','丙','午','丁','未','坤','申','庚','酉','辛','戌','乾','亥','壬'];
const ELEMENTS = {'子':'水','癸':'水','壬':'水','亥':'水','午':'火','丁':'火','丙':'火','巳':'火','卯':'木','乙':'木','甲':'木','寅':'木','酉':'金','辛':'金','庚':'金','申':'金','艮':'土','坤':'土','辰':'土','戌':'土','未':'土','丑':'土','巽':'木','乾':'金'};

// ★あなたの最新のGAS URL
const GAS_URL = "https://script.google.com/macros/s/AKfycbz3ROMlDSXoeAF4ETtTJqDzp6uJMJQdXe4l2EMDiKre-AKLV9D09EC5n_o56DznCgLm/exec";

export const fetchDirectionInfo = async (angle) => {
  const index = Math.floor(((angle + 7.5) % 360) / 15);
  const mountain = MOUNTAINS[index];
  return { result: { mountain, element: ELEMENTS[mountain] || "不明" } };
};

export const saveToSpreadsheet = async (data) => {
  try {
    const params = new URLSearchParams(data).toString();
    await fetch(`${GAS_URL}?${params}`, { method: "GET", mode: "no-cors" });
    return true;
  } catch (e) { return false; }
};

export const getMapUrl = (mode) => {
  return new Promise((resolve) => {
    navigator.geolocation.getCurrentPosition((pos) => {
      const { latitude, longitude } = pos.coords;
      const url = mode === 'gsi' 
        ? `https://maps.gsi.go.jp/#16/${latitude}/${longitude}/`
        : `https://maps.google.com/maps?q=${latitude},${longitude}&z=16&output=embed`;
      resolve(url);
    }, () => resolve(mode === 'gsi' ? "https://maps.gsi.go.jp/" : "https://maps.google.com/maps?output=embed"));
  });
};

// 【新機能】四柱推命 AI 鑑定
export const getShiShuDivination = async (natalChart, userQuery, useMock = false) => {
  const backendUrl = process.env.REACT_APP_BACKEND_URL || "http://localhost:5000";
  
  try {
    const response = await fetch(`${backendUrl}/api/divination/ai-reading`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        natal_chart: natalChart,
        user_query: userQuery,
        use_mock: useMock
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error("四柱推命 API エラー:", error);
    return {
      status: "error",
      message: `API呼び出し失敗: ${error.message}`,
      divination: "申し訳ございません。現在、鑑定サービスが利用できません。"
    };
  }
};

// 【ヘルパー】生年月日から命盤データを生成（簡易版）
export const generateNatalChart = (year, month, day, hour = null, gender = '不明') => {
  // 実装例：四柱推命の命盤計算は fortune-core と連携する想定
  // ここは簡易版のデータ構造
  return {
    year_pillar: `${year}年`,
    month_pillar: `${month}月`,
    day_pillar: `${day}日`,
    hour_pillar: hour ? `${hour}時` : null,
    gender: gender,
    timestamp: `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}${hour ? `T${String(hour).padStart(2, '0')}:00:00` : ''}`
  };
};