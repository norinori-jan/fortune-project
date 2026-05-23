// ExportEngine.ts
// Fortune Workstation — Obsidian Canvas / CSV 出力エンジン
// event.id を Canvas写真素材との「アンカー」として機能させるデータ構造

// ============================================================
// § 1. アンカーID設計
// ============================================================
//
// 【設計方針】
// ObsidianのCanvas (.canvas) は JSON形式。各ノードは "id" フィールドを持ち、
// edgesで相互参照する。写真素材（file node）と占術記録（text node）を
// 同一IDプレフィックスで紐付けることで、後から Canvas上でエッジを引ける。
//
// ID形式: {prefix}-{YYYYMMDD}-{HHMMSS}-{seq3}
//   例: FW-20250615-143022-001
//       FW = Fortune Workstation
//       20250615 = 占断日
//       143022 = 起卦時刻
//       001 = セッション内連番
//
// 写真アンカー形式: {eventId}-img-{n3}
//   例: FW-20250615-143022-001-img-001  ← 1枚目の写真ノード
//       FW-20250615-143022-001-img-002  ← 2枚目
//
// この設計により:
//   - Obsidian Canvas上で占術ノードを検索→対応写真を一意特定
//   - ファイル名にも同IDを使用すれば、ファイルシステムでも追跡可能
//   - 将来的なDBインデックスとして機能

// ============================================================
// § 2. 型定義
// ============================================================

/** Fortune Workstation 共通イベントID */
export type FortuneEventId = string; // "FW-YYYYMMDD-HHMMSS-NNN"

/** 写真アンカーID */
export type ImageAnchorId = string;  // "{eventId}-img-NNN"

/** 占術種別 */
export type DivinationType = "梅花心易" | "玄空飛星" | "奇門遁甲" | "紫微斗数" | "その他";

// ── 核心: FortuneEvent ──────────────────────────────────────

/**
 * 占術記録の最小単位。
 * すべての出力形式（Canvas / CSV / Obsidian Note）の共通ソース。
 */
export interface FortuneEvent {
  /** Obsidian Canvas・ファイル名・DBキーとして使う共通アンカーID */
  id: FortuneEventId;

  /** IDから自動復元できるが利便性のため保持 */
  timestamp: Date;
  sequenceInSession: number;  // セッション内連番 (1〜999)

  /** 占術メタデータ */
  divinationType: DivinationType;
  question: string;          // 占問（ユーザー入力）
  location?: string;         // 観測地点（任意）

  /** 占断結果（型は種別によって異なる） */
  result: DivinationResult;

  /** 紐付け画像のアンカーIDリスト（後から追加可能） */
  imageAnchors: ImageAnchorId[];

  /** Obsidian フロントマター用タグ */
  tags: string[];

  /** 自由メモ */
  notes: string;
}

/** 占断結果の共用型 */
export type DivinationResult =
  | MeihuaResult
  | FengShuiResult
  | GenericResult;

export interface MeihuaResult {
  type: "梅花心易";
  upperTrigram: string;      // "坎"
  lowerTrigram: string;      // "坎"
  movingLine: number;        // 1〜6
  hexagramName?: string;
  calculationLog: string;    // formatCalculationLog の出力
}

export interface FengShuiResult {
  type: "玄空飛星";
  sitting: string;           // 坐山 例: "壬"
  facing: string;            // 向首 例: "丙"
  period: number;            // 元運 1〜9
  layerIds: number[];        // 参照した羅盤層ID
  analysis: string;
}

export interface GenericResult {
  type: "その他";
  summary: string;
  rawData?: Record<string, unknown>;
}

// ── Canvas ノード型 ─────────────────────────────────────────

/** Obsidian Canvas の text ノード */
export interface CanvasTextNode {
  id: string;
  type: "text";
  text: string;
  x: number;
  y: number;
  width: number;
  height: number;
  color?: string;  // "1"〜"6" or hex
}

/** Obsidian Canvas の file ノード（写真等） */
export interface CanvasFileNode {
  id: string;
  type: "file";
  file: string;    // Vaultからの相対パス
  x: number;
  y: number;
  width: number;
  height: number;
}

/** Obsidian Canvas の edge */
export interface CanvasEdge {
  id: string;
  fromNode: string;
  fromSide: "top"|"right"|"bottom"|"left";
  toNode: string;
  toSide: "top"|"right"|"bottom"|"left";
  label?: string;
}

/** .canvas ファイルの最上位構造 */
export interface ObsidianCanvas {
  nodes: (CanvasTextNode | CanvasFileNode)[];
  edges: CanvasEdge[];
}

// ============================================================
// § 3. ID生成ロジック
// ============================================================

/** セッション内連番を管理するカウンター（シングルトン） */
class SessionSequence {
  private counter = 0;
  reset() { this.counter = 0; }
  next(): number { return ++this.counter; }
}
export const sessionSequence = new SessionSequence();

/**
 * FortuneEventId を生成する
 * @param date 起卦日時（Date インスタンスであること。文字列を渡すと自動変換）
 * @param seq  省略時は sessionSequence.next() を使用
 *
 * @throws {TypeError} date が Date に変換できない値の場合
 *
 * ### [object Object] バグについて
 * `pad()` は `String(n)` を使う。`n` に Date や ShizhiResult 等の
 * オブジェクトが混入すると `"[object Object]"` になる。
 * 以下の防御的ガードでこれを防ぐ。
 */
export function generateEventId(date: Date, seq?: number): FortuneEventId {
  // ── 防御ガード ────────────────────────────────────────────────
  // date が Date 以外（文字列・number・object）の場合は強制変換
  const safeDate: Date = date instanceof Date ? date : new Date(date as never);
  if (isNaN(safeDate.getTime())) {
    throw new TypeError(
      `generateEventId: invalid date argument "${String(date)}". ` +
      "Pass a Date instance, e.g. new Date()."
    );
  }
  // seq が number でない場合（ShizhiResult 等が誤って渡された場合）を防ぐ
  const safeSeq: number =
    typeof seq === "number" && Number.isFinite(seq) && seq > 0
      ? Math.floor(seq)
      : sessionSequence.next();
  // ── ID 組み立て ───────────────────────────────────────────────
  const pad = (n: number, d = 2): string => String(Math.floor(n)).padStart(d, "0");
  const YYYY = safeDate.getFullYear();
  const MM   = pad(safeDate.getMonth() + 1);
  const DD   = pad(safeDate.getDate());
  const hh   = pad(safeDate.getHours());
  const mm   = pad(safeDate.getMinutes());
  const ss   = pad(safeDate.getSeconds());
  const NNN  = pad(safeSeq, 3);
  return `FW-${YYYY}${MM}${DD}-${hh}${mm}${ss}-${NNN}`;
}

/**
 * 画像アンカーIDを生成する
 * @param eventId 親イベントのID
 * @param imageIndex 1-indexed
 */
export function generateImageAnchorId(
  eventId: FortuneEventId,
  imageIndex: number
): ImageAnchorId {
  return `${eventId}-img-${String(imageIndex).padStart(3, "0")}`;
}

/**
 * EventIdからタイムスタンプ情報を復元する（ファイル名等からの逆引き）
 */
export function parseEventId(id: FortuneEventId): {
  date: Date;
  seq: number;
} | null {
  const m = id.match(/^FW-(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})(\d{2})-(\d{3})$/);
  if (!m) return null;
  const [, Y, Mo, D, h, mi, s, seq] = m;
  return {
    date: new Date(+Y, +Mo-1, +D, +h, +mi, +s),
    seq: parseInt(seq, 10),
  };
}

// ============================================================
// § 4. FortuneEvent ファクトリ
// ============================================================

export function createFortuneEvent(params: {
  date?: Date;
  divinationType: DivinationType;
  question: string;
  result: DivinationResult;
  location?: string;
  tags?: string[];
  notes?: string;
  seq?: number;
}): FortuneEvent {
  const date = params.date instanceof Date ? params.date : new Date();
  // seq を先に確定させてから generateEventId に渡す。
  // こうしないと generateEventId 内の `seq ?? sessionSequence.next()` が
  // 二重カウントを起こす可能性がある。
  const seq = typeof params.seq === "number" ? params.seq : sessionSequence.next();
  const id  = generateEventId(date, seq);  // seq は必ず number として渡す

  return {
    id,
    timestamp: date,
    sequenceInSession: seq,
    divinationType: params.divinationType,
    question: params.question,
    location: params.location,
    result: params.result,
    imageAnchors: [],
    tags: params.tags ?? [params.divinationType],
    notes: params.notes ?? "",
  };
}

/** 既存イベントに画像アンカーを追加する（イミュータブル） */
export function attachImageAnchor(
  event: FortuneEvent,
  imageIndex: number
): FortuneEvent {
  const anchorId = generateImageAnchorId(event.id, imageIndex);
  if (event.imageAnchors.includes(anchorId)) return event;
  return { ...event, imageAnchors: [...event.imageAnchors, anchorId] };
}

// ============================================================
// § 5. Obsidian Canvas エクスポーター
// ============================================================

const CANVAS_LAYOUT = {
  NODE_WIDTH:  400,
  NODE_HEIGHT: 300,
  IMAGE_WIDTH: 300,
  IMAGE_HEIGHT: 200,
  X_GAP: 60,
  Y_STRIDE: 400,  // イベント間の縦間隔
};

/**
 * FortuneEvent[] → .canvas JSON
 *
 * レイアウト:
 *   [占術テキストノード]  [画像ノード1] [画像ノード2] ...
 *      ↑eventId              ↑imageAnchor1    ↑imageAnchor2
 *   エッジで接続
 */
export function exportToCanvas(
  events: FortuneEvent[],
  options: {
    imageVaultRoot?: string;  // Vault内の画像フォルダパス ("Attachments/fortune")
    colorScheme?: Record<DivinationType, string>;
  } = {}
): ObsidianCanvas {
  const { imageVaultRoot = "Attachments/fortune" } = options;
  const defaultColors: Record<DivinationType, string> = {
    "梅花心易": "4",   // green
    "玄空飛星": "3",   // yellow
    "奇門遁甲": "1",   // red
    "紫微斗数": "6",   // purple
    "その他":   "0",   // default
    ...options.colorScheme,
  };

  const nodes: (CanvasTextNode | CanvasFileNode)[] = [];
  const edges: CanvasEdge[] = [];

  events.forEach((event, i) => {
    const baseY = i * CANVAS_LAYOUT.Y_STRIDE;
    const textNodeId = event.id;  // ← 占術ノードのIDはそのままeventId

    // ① 占術テキストノード
    const textContent = formatCanvasNodeText(event);
    nodes.push({
      id: textNodeId,
      type: "text",
      text: textContent,
      x: 0,
      y: baseY,
      width: CANVAS_LAYOUT.NODE_WIDTH,
      height: CANVAS_LAYOUT.NODE_HEIGHT,
      color: defaultColors[event.divinationType] ?? "0",
    });

    // ② 画像ノード（アンカーID付き）
    event.imageAnchors.forEach((anchorId, j) => {
      const imgX = CANVAS_LAYOUT.NODE_WIDTH + CANVAS_LAYOUT.X_GAP
                 + j * (CANVAS_LAYOUT.IMAGE_WIDTH + CANVAS_LAYOUT.X_GAP);
      const imgPath = `${imageVaultRoot}/${anchorId}.jpg`;

      nodes.push({
        id: anchorId,  // ← 画像ノードのIDはimageAnchorId
        type: "file",
        file: imgPath,
        x: imgX,
        y: baseY + (CANVAS_LAYOUT.NODE_HEIGHT - CANVAS_LAYOUT.IMAGE_HEIGHT) / 2,
        width: CANVAS_LAYOUT.IMAGE_WIDTH,
        height: CANVAS_LAYOUT.IMAGE_HEIGHT,
      });

      // ③ 占術ノード → 画像ノード のエッジ
      edges.push({
        id: `edge-${textNodeId}-${anchorId}`,
        fromNode: textNodeId,
        fromSide: "right",
        toNode: anchorId,
        toSide: "left",
        label: `img-${String(j+1).padStart(3,"0")}`,
      });
    });
  });

  return { nodes, edges };
}

/** Canvas テキストノードの本文を生成 */
function formatCanvasNodeText(event: FortuneEvent): string {
  const lines: string[] = [
    `# ${event.divinationType}`,
    `**ID**: \`${event.id}\``,
    `**日時**: ${event.timestamp.toLocaleString("ja-JP")}`,
    `**占問**: ${event.question}`,
  ];

  if (event.location) lines.push(`**地点**: ${event.location}`);

  lines.push("---");

  switch (event.result.type) {
    case "梅花心易": {
      const r = event.result;
      lines.push(`**本卦**: 上${r.upperTrigram} / 下${r.lowerTrigram}`);
      lines.push(`**動爻**: 第${r.movingLine}爻`);
      if (r.hexagramName) lines.push(`**卦名**: ${r.hexagramName}`);
      lines.push("```");
      lines.push(r.calculationLog);
      lines.push("```");
      break;
    }
    case "玄空飛星": {
      const r = event.result;
      lines.push(`**坐**: ${r.sitting}  **向**: ${r.facing}`);
      lines.push(`**元運**: 第${r.period}運`);
      lines.push(`**参照層**: L${r.layerIds.join(", L")}`);
      lines.push(r.analysis);
      break;
    }
    default: {
      lines.push(event.result.summary);
    }
  }

  if (event.notes) {
    lines.push("---");
    lines.push(`**メモ**: ${event.notes}`);
  }

  if (event.tags.length) {
    lines.push(event.tags.map(t => `#${t}`).join(" "));
  }

  return lines.join("\n");
}

// ============================================================
// § 6. CSV エクスポーター
// ============================================================

const CSV_COLUMNS = [
  "id", "timestamp", "divinationType", "question",
  "location", "result_summary", "imageAnchors", "tags", "notes",
] as const;

export function exportToCSV(events: FortuneEvent[]): string {
  const escape = (s: string) => `"${String(s ?? "").replace(/"/g, '""')}"`;
  const header = CSV_COLUMNS.join(",");

  const rows = events.map(e => {
    const resultSummary = (() => {
      switch (e.result.type) {
        case "梅花心易":  return `上${e.result.upperTrigram}/下${e.result.lowerTrigram} 第${e.result.movingLine}爻動`;
        case "玄空飛星":  return `${e.result.sitting}坐${e.result.facing}向 第${e.result.period}運`;
        // GenericResult.summary が undefined の場合も空文字にフォールスルー
        default:         return (e.result as { summary?: string }).summary ?? "";
      }
    })();

    return [
      escape(e.id),
      escape(e.timestamp instanceof Date ? e.timestamp.toISOString() : String(e.timestamp)),
      escape(e.divinationType),
      escape(e.question),
      escape(e.location ?? ""),
      escape(resultSummary),
      escape(e.imageAnchors.join("|")),
      escape(e.tags.join("|")),
      escape(e.notes),
    ].join(",");
  });

  return [header, ...rows].join("\n");
}

// ============================================================
// § 7. Obsidian Markdown Note エクスポーター
// ============================================================

export function exportToObsidianNote(event: FortuneEvent): string {
  // toTimeString() はローカルタイムゾーン依存で環境により結果が変わる。
  // toISOString() でUTC文字列を取り、必要な部分をスライスする（一貫性確保）。
  const safeDate = event.timestamp instanceof Date
    ? event.timestamp
    : new Date(event.timestamp as never);
  const isoStr  = safeDate.toISOString();              // "2025-06-15T14:30:22.000Z"
  const dateStr = isoStr.split("T")[0];                // "2025-06-15"
  const timeStr = isoStr.split("T")[1].slice(0, 8);   // "14:30:22"

  const fm: string[] = [
    "---",
    `id: "${event.id}"`,
    `date: ${dateStr}`,
    `time: ${timeStr}`,
    `type: ${event.divinationType}`,
    `tags: [${event.tags.map(t => `"${t}"`).join(", ")}]`,
    `imageAnchors: [${event.imageAnchors.map(a => `"${a}"`).join(", ")}]`,
    "---",
  ];

  const body = formatCanvasNodeText(event);
  return [...fm, "", body].join("\n");
}

// ============================================================
// § 8. 使用例
// ============================================================

/*
import { calculateHexagram, formatCalculationLog } from "./YiEngine";
import {
  createFortuneEvent, attachImageAnchor,
  exportToCanvas, exportToCSV, exportToObsidianNote,
} from "./ExportEngine";

// 占断実行
const hexResult = calculateHexagram({
  date: new Date("2025-06-15T14:30:00"),
  eventNumber: 3,
});

// FortuneEvent 作成
let event = createFortuneEvent({
  divinationType: "梅花心易",
  question: "この事業の行方は？",
  result: {
    type: "梅花心易",
    upperTrigram: hexResult.upperTrigram.name,
    lowerTrigram: hexResult.lowerTrigram.name,
    movingLine: hexResult.movingLine,
    calculationLog: formatCalculationLog(hexResult),
  },
  tags: ["梅花心易", "事業", "2025"],
});

// 画像アンカーを付与（3枚の写真と紐付け）
event = attachImageAnchor(event, 1);
event = attachImageAnchor(event, 2);
event = attachImageAnchor(event, 3);

console.log("Event ID:", event.id);
// → "FW-20250615-143000-001"

console.log("Image anchors:", event.imageAnchors);
// → ["FW-20250615-143000-001-img-001", "FW-20250615-143000-001-img-002", "FW-20250615-143000-001-img-003"]

// Canvas出力
const canvas = exportToCanvas([event], { imageVaultRoot: "占術/素材" });
const canvasJson = JSON.stringify(canvas, null, 2);
// → 写真ファイルは "占術/素材/FW-20250615-143000-001-img-001.jpg" として保存すれば自動紐付け

// CSV出力
const csv = exportToCSV([event]);

// Obsidian Note出力
const note = exportToObsidianNote(event);
*/