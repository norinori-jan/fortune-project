/**
 * app.js — 人相鑑定（天童流）フェーズ①
 * ─────────────────────────────────────────────
 * 写真をアップロード → MediaPipe Face Landmarkerで顔特徴点を検出
 * → 三停（上停・中停・下停）を算出してcanvasに重ねて表示する。
 *
 * 【三停の算出方法（重要）】
 * MediaPipeの顔メッシュは「眉〜顎」までは高精度に検出できるが、
 * 「生え際」は髪型に隠れるため顔メッシュのモデルに含まれておらず、
 * 直接検出できない。
 * そこで天童流の古典的な考え方「上停・中停・下停はおおむね等しい
 * 長さになる」を利用し、実測できる中停・下停の長さの平均を
 * 上停の推定値として使い、眉のラインから逆算して生え際の推定位置を出す。
 * この推定である旨は画面上に明示する。
 */

import {
  FaceLandmarker,
  FilesetResolver,
} from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/vision_bundle.mjs";

// ── MediaPipe 顔メッシュの参照点インデックス ──
// (468/478点モデルの標準トポロジー。公式ドキュメントに準拠)
const LM = {
  browLeft: 55,      // 左眉（内側寄り）
  browRight: 285,     // 右眉（内側寄り）
  glabella: 9,        // 眉間（印堂付近）
  noseTip: 4,          // 鼻尖
  noseBase: 2,         // 鼻下（人中の起点、準頭〜人中境目付近）
  chin: 152,           // 顎先（地閣）
  faceLeft: 234,       // 顔の左端
  faceRight: 454,      // 顔の右端
  foreheadTop: 10,     // 顔メッシュ最上部（生え際そのものではない事に注意）
};

const $ = (id) => document.getElementById(id);
const fileInput = $("fileInput");
const uploadArea = $("uploadArea");
const uploadLabel = $("uploadLabel");
const resultCard = $("resultCard");
const canvas = $("outputCanvas");
const ctx = canvas.getContext("2d");
const statusLine = $("statusLine");
const zoneList = $("zoneList");
const resetBtn = $("resetBtn");
const toggleRow = $("toggleRow");

let faceLandmarker = null;
let currentImage = null;
let currentLandmarks = null;
let activeLayers = { santei: true, landmarks: false };

// ═══════════════════════════════════
// 初期化：MediaPipe FaceLandmarkerをロード
// ═══════════════════════════════════
async function initFaceLandmarker() {
  setStatus("顔検出モデルを準備中…", "");
  try {
    const vision = await FilesetResolver.forVisionTasks(
      "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14/wasm"
    );
    try {
      faceLandmarker = await FaceLandmarker.createFromOptions(vision, {
        baseOptions: {
          modelAssetPath:
            "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task",
          delegate: "GPU",
        },
        outputFaceBlendshapes: false,
        runningMode: "IMAGE",
        numFaces: 1,
      });
    } catch (gpuErr) {
      // FIX: GPUデリゲートが使えない環境（一部のブラウザ・PC）向けにCPUへフォールバック
      console.warn("GPU delegateの初期化に失敗、CPUで再試行します:", gpuErr);
      faceLandmarker = await FaceLandmarker.createFromOptions(vision, {
        baseOptions: {
          modelAssetPath:
            "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task",
          delegate: "CPU",
        },
        outputFaceBlendshapes: false,
        runningMode: "IMAGE",
        numFaces: 1,
      });
    }
    setStatus("準備完了。写真を選んでください", "ok");
  } catch (err) {
    console.error(err);
    setStatus(
      "顔検出モデルの読み込みに失敗しました。通信環境を確認してください。",
      "err"
    );
  }
}

function setStatus(msg, kind) {
  statusLine.textContent = msg;
  statusLine.className = "status-line" + (kind ? " " + kind : "");
}

// ═══════════════════════════════════
// ファイル選択・ドラッグ&ドロップ
// ═══════════════════════════════════
fileInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (file) handleImageFile(file);
});
uploadArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  uploadArea.classList.add("drag");
});
uploadArea.addEventListener("dragleave", () => uploadArea.classList.remove("drag"));
uploadArea.addEventListener("drop", (e) => {
  e.preventDefault();
  uploadArea.classList.remove("drag");
  const file = e.dataTransfer.files[0];
  if (file && file.type.startsWith("image/")) handleImageFile(file);
});

resetBtn.addEventListener("click", () => {
  resultCard.style.display = "none";
  resetBtn.style.display = "none";
  uploadLabel.innerHTML =
    '📷 正面から撮った顔写真を選んでください<br /><span style="font-size:11px">できるだけ明るい場所で、髪を上げて額が見える写真がおすすめです</span>';
  fileInput.value = "";
  currentImage = null;
  currentLandmarks = null;
});

toggleRow.addEventListener("click", (e) => {
  const btn = e.target.closest(".toggle-chip");
  if (!btn) return;
  const layer = btn.dataset.layer;
  activeLayers[layer] = !activeLayers[layer];
  btn.classList.toggle("active", activeLayers[layer]);
  if (currentImage && currentLandmarks) render();
});

// ═══════════════════════════════════
// 画像読み込み → 顔検出 → 描画
// ═══════════════════════════════════
async function handleImageFile(file) {
  if (!faceLandmarker) {
    setStatus("顔検出モデルの準備がまだ終わっていません。少し待ってから再度お試しください。", "err");
    return;
  }

  setStatus("画像を読み込み中…", "");
  const img = new Image();
  const url = URL.createObjectURL(file);

  img.onload = () => {
    URL.revokeObjectURL(url);
    currentImage = img;
    resultCard.style.display = "block";
    resetBtn.style.display = "block";
    detectFace(img);
  };
  img.onerror = () => {
    setStatus("画像を読み込めませんでした。別のファイルをお試しください。", "err");
  };
  img.src = url;
}

function detectFace(img) {
  setStatus("顔を検出中…", "");
  try {
    const result = faceLandmarker.detect(img);
    if (!result.faceLandmarks || result.faceLandmarks.length === 0) {
      setStatus(
        "顔を検出できませんでした。正面を向いた、顔全体が写っている写真でお試しください。",
        "err"
      );
      currentLandmarks = null;
      drawImageOnly(img);
      return;
    }
    currentLandmarks = result.faceLandmarks[0];
    setStatus("検出できました。以下に三停を表示します。", "ok");
    render();
  } catch (err) {
    console.error(err);
    setStatus("顔検出中にエラーが発生しました: " + err.message, "err");
  }
}

function drawImageOnly(img) {
  canvas.width = img.naturalWidth;
  canvas.height = img.naturalHeight;
  ctx.drawImage(img, 0, 0);
}

// ═══════════════════════════════════
// 三停の算出
// ═══════════════════════════════════
/**
 * 検出済みランドマーク（正規化座標 0〜1）から三停の各Y座標を算出する。
 * @param {Array<{x:number,y:number}>} landmarks
 * @param {number} imgW 画像の実ピクセル幅
 * @param {number} imgH 画像の実ピクセル高さ
 */
function computeSantei(landmarks, imgW, imgH) {
  const toPx = (lm) => ({ x: lm.x * imgW, y: lm.y * imgH });

  const browL = toPx(landmarks[LM.browLeft]);
  const browR = toPx(landmarks[LM.browRight]);
  const noseBase = toPx(landmarks[LM.noseBase]);
  const chin = toPx(landmarks[LM.chin]);
  const faceL = toPx(landmarks[LM.faceLeft]);
  const faceR = toPx(landmarks[LM.faceRight]);

  const browY = (browL.y + browR.y) / 2; // 上停/中停の境界（実測）
  const noseBaseY = noseBase.y;          // 中停/下停の境界（実測）
  const chinY = chin.y;                   // 下停の下端（実測）

  const chuutei = noseBaseY - browY; // 中停の長さ（実測）
  const katei = chinY - noseBaseY;   // 下停の長さ（実測）

  // FIX: 生え際は検出できないため、天童流の「三停は概ね等しい」という
  // 考え方を使い、中停・下停の平均を上停の推定長とする
  const joteiEstimated = (chuutei + katei) / 2;
  const hairlineYEstimated = browY - joteiEstimated;

  const widthLeft = Math.min(faceL.x, faceR.x);
  const widthRight = Math.max(faceL.x, faceR.x);

  return {
    hairlineY: hairlineYEstimated,
    browY,
    noseBaseY,
    chinY,
    left: widthLeft,
    right: widthRight,
    lengths: { jotei: joteiEstimated, chuutei, katei },
  };
}

// ═══════════════════════════════════
// 描画
// ═══════════════════════════════════
function render() {
  const img = currentImage;
  const landmarks = currentLandmarks;
  canvas.width = img.naturalWidth;
  canvas.height = img.naturalHeight;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(img, 0, 0);

  if (!landmarks) return;

  if (activeLayers.landmarks) {
    drawLandmarks(landmarks, canvas.width, canvas.height);
  }

  if (activeLayers.santei) {
    const santei = computeSantei(landmarks, canvas.width, canvas.height);
    drawSantei(santei);
    renderZoneList(santei);
  } else {
    zoneList.innerHTML = "";
  }
}

function drawLandmarks(landmarks, w, h) {
  ctx.fillStyle = "rgba(127,119,221,0.55)";
  for (const lm of landmarks) {
    ctx.beginPath();
    ctx.arc(lm.x * w, lm.y * h, 1.2, 0, Math.PI * 2);
    ctx.fill();
  }
}

function drawSantei(s) {
  const lineDefs = [
    { y: s.hairlineY, label: "生え際（推定）", estimated: true, color: "#ef9f27" },
    { y: s.browY, label: "眉（上停/中停の境）", estimated: false, color: "#7f77dd" },
    { y: s.noseBaseY, label: "鼻下（中停/下停の境）", estimated: false, color: "#7f77dd" },
    { y: s.chinY, label: "顎先", estimated: false, color: "#7f77dd" },
  ];

  ctx.lineWidth = Math.max(2, canvas.width * 0.003);
  ctx.font = `${Math.max(14, canvas.width * 0.025)}px sans-serif`;
  ctx.textBaseline = "bottom";

  for (const line of lineDefs) {
    ctx.strokeStyle = line.color;
    ctx.setLineDash(line.estimated ? [8, 6] : []);
    ctx.beginPath();
    ctx.moveTo(s.left, line.y);
    ctx.lineTo(s.right, line.y);
    ctx.stroke();

    ctx.fillStyle = line.color;
    ctx.fillText(line.label, s.left, line.y - 4);
  }
  ctx.setLineDash([]);
}

// ═══════════════════════════════════
// 部位リストの表示（テキスト情報パネル）
// ═══════════════════════════════════
const SANTEI_INFO = [
  {
    key: "jotei",
    name: "上停",
    color: "#ef9f27",
    estimated: true,
    ageRange: "1〜20歳（初年）",
    desc: "生え際〜眉。先祖・両親・目上との縁、若年期の運勢を見る。額が広く豊かであれば初年運が良いとされる。",
  },
  {
    key: "chuutei",
    name: "中停",
    color: "#7f77dd",
    estimated: false,
    ageRange: "21〜42歳（中年）",
    desc: "眉〜鼻下。目・鼻を中心とした、中年期の自立・仕事・財運を見る。鼻筋が通り、肉付きが良ければ中年運が良いとされる。",
  },
  {
    key: "katei",
    name: "下停",
    color: "#7f77dd",
    estimated: false,
    ageRange: "43〜60歳（晩年）",
    desc: "鼻下〜顎先。口・顎を中心とした、晩年期の家庭運・晩年の安定を見る。顎が豊かであれば晩年運が良いとされる。",
  },
];

function renderZoneList(santei) {
  zoneList.innerHTML = SANTEI_INFO.map((info) => {
    const lengthPx = santei.lengths[info.key];
    return `
      <div class="zone-item">
        <span class="zone-dot" style="background:${info.color}"></span>
        <span class="zone-name">${info.name}</span>
        <span class="zone-desc">${info.desc}<br><span style="color:var(--text3)">${info.ageRange}</span></span>
        ${info.estimated ? '<span class="zone-est">推定</span>' : ""}
      </div>
    `;
  }).join("");
}

// ═══════════════════════════════════
// 初期化実行
// ═══════════════════════════════════
initFaceLandmarker();