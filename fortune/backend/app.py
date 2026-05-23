"""
易（周易）占いアプリ — Flask バックエンド API
"""

import json
import os
import random
import re
import sqlite3
from io import StringIO
from datetime import datetime
from urllib import error, request as urllib_request
import csv

from flask import Flask, jsonify, redirect, request, send_from_directory, Response
from flask_cors import CORS
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from hexagrams import (
    get_hexagram,
    get_changing_hexagram,
    get_line_names,
    TRIGRAMS,
)

# AI鑑定モジュール
try:
    from ai_divination.divination_service import DivinationService
except ImportError:
    DivinationService = None

# backend/.env を読み込む
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# フロントエンドのビルド済みファイルのパス
FRONTEND_DIST = os.path.join(
    os.path.dirname(__file__), '..', 'frontend', 'dist'
)
DB_PATH = os.environ.get(
    'DB_PATH',
    os.path.join(os.path.dirname(__file__), 'divinations.db')
)
SHEETS_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

app = Flask(
    __name__,
    static_folder=FRONTEND_DIST,
    static_url_path='/',
)
CORS(app)

# AI鑑定サービスの初期化
divination_service = None
if DivinationService:
    try:
        divination_service = DivinationService()
    except Exception as e:
        print(f"Warning: DivinationService初期化エラー: {e}")


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS divinations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_name TEXT NOT NULL,
                question TEXT NOT NULL,
                created_at TEXT NOT NULL,
                lower_number INTEGER NOT NULL,
                upper_number INTEGER NOT NULL,
                changing_line INTEGER NOT NULL,
                honke_name TEXT NOT NULL,
                shike_name TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT '総合',
                ai_response TEXT NOT NULL,
                feedback TEXT NOT NULL DEFAULT '',
                self_score INTEGER
            )
            """
        )

        # 既存DBとの互換: self_score列が無ければ追加
        cols = {
            row['name'] for row in conn.execute("PRAGMA table_info(divinations)").fetchall()
        }
        if 'self_score' not in cols:
            conn.execute("ALTER TABLE divinations ADD COLUMN self_score INTEGER")

        if 'evaluated_at' not in cols:
            conn.execute("ALTER TABLE divinations ADD COLUMN evaluated_at TEXT")

        if 'category' not in cols:
            conn.execute("ALTER TABLE divinations ADD COLUMN category TEXT NOT NULL DEFAULT '総合'")

        conn.commit()


def _infer_category_from_question(question: str) -> str:
    match = re.match(r"^【([^】]+)】", question or "")
    if match:
        return match.group(1).strip() or '総合'
    return '総合'


def generate_gemini_response(person_name: str, question: str, honke: dict, shike: dict, changing_line: int, changing_line_name: str) -> str:
    """Gemini で占断文を生成。失敗時はテンプレート文を返す。"""
    fallback = (
        f"{person_name}さんのテーマ『{question}』について、"
        f"本卦 {honke['name']} から之卦 {shike['name']} への変化（{changing_line_name}）が示されました。"
        "まずは短期の変化を観察し、後日フィードバックで実際との差分を記録してください。"
    )

    api_key = os.environ.get('GOOGLE_API_KEY', '').strip()
    if not api_key:
        return fallback

    prompt = f"""
あなたは周易占断アシスタントです。日本語で簡潔に答えてください。
対象者: {person_name}
相談内容: {question}
本卦: 第{honke['number']}卦 {honke['name']}（{honke['meaning']}）
之卦: 第{shike['number']}卦 {shike['name']}（{shike['meaning']}）
変爻: {changing_line_name}（第{changing_line}爻）

出力要件:
1) 現状解釈
2) 今後1〜3か月の見立て
3) 具体的行動アドバイス（3点）
4) 検証用チェックポイント（後日比較できる観測項目）
""".strip()

    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/gemini-2.0-flash:generateContent?key={api_key}"
    )
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    req = urllib_request.Request(
        endpoint,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )

    try:
        with urllib_request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            candidates = data.get('candidates', [])
            if not candidates:
                return fallback
            parts = candidates[0].get('content', {}).get('parts', [])
            text = ''.join(p.get('text', '') for p in parts).strip()
            return text or fallback
    except (error.URLError, error.HTTPError, TimeoutError, json.JSONDecodeError):
        return fallback


def serialize_divination_row(row: sqlite3.Row) -> dict:
    lower = row['lower_number']
    upper = row['upper_number']
    changing_line = row['changing_line']
    honke = get_hexagram(lower, upper)
    shike = get_changing_hexagram(lower, upper, changing_line)
    line_names = get_line_names()
    return {
        'id': row['id'],
        'person_name': row['person_name'],
        'question': row['question'],
        'category': row['category'],
        'created_at': row['created_at'],
        'lower_number': lower,
        'upper_number': upper,
        'changing_line': changing_line,
        'changing_line_name': line_names[changing_line],
        'honke': honke,
        'shike': shike,
        'ai_response': row['ai_response'],
        'feedback': row['feedback'],
        'self_score': row['self_score'],
        'evaluated_at': row['evaluated_at'],
        'hexagram_summary': f"本卦:{honke['name']}（{honke['meaning']}） / 之卦:{shike['name']}（{shike['meaning']}） / 変爻:{line_names[changing_line]}",
    }


def _build_divinations_filters(args) -> tuple[str, list]:
    clauses = []
    params = []

    person_name = (args.get('person_name') or '').strip()
    keyword = (args.get('keyword') or '').strip()
    from_date = (args.get('from_date') or '').strip()
    to_date = (args.get('to_date') or '').strip()
    min_score_raw = (args.get('min_score') or '').strip()
    max_score_raw = (args.get('max_score') or '').strip()

    if person_name:
        clauses.append("person_name LIKE ?")
        params.append(f"%{person_name}%")

    if keyword:
        clauses.append("question LIKE ?")
        params.append(f"%{keyword}%")

    if from_date:
        clauses.append("date(created_at) >= date(?)")
        params.append(from_date)

    if to_date:
        clauses.append("date(created_at) <= date(?)")
        params.append(to_date)

    if min_score_raw:
        try:
            min_score = int(min_score_raw)
            clauses.append("self_score >= ?")
            params.append(min_score)
        except ValueError:
            pass

    if max_score_raw:
        try:
            max_score = int(max_score_raw)
            clauses.append("self_score <= ?")
            params.append(max_score)
        except ValueError:
            pass

    where_clause = ''
    if clauses:
        where_clause = 'WHERE ' + ' AND '.join(clauses)

    return where_clause, params


def _csv_safe(value):
    """Google Sheets/Excel向けに数式注入を抑止する。"""
    if value is None:
        return ''
    text = str(value)
    if text.startswith(('=', '+', '-', '@')):
        return "'" + text
    return text


def _summarize_ai_response(text: str, max_len: int = 120) -> str:
    if not text:
        return ''
    one_line = ' '.join(str(text).split())
    if len(one_line) <= max_len:
        return one_line
    return one_line[: max_len - 1] + '…'


def _get_google_creds():
    """環境変数から Service Account 資格情報を構築する。"""
    json_str = (os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON') or '').strip()
    file_path = (os.environ.get('GOOGLE_SERVICE_ACCOUNT_FILE') or '').strip()

    if json_str:
        info = json.loads(json_str)
        return service_account.Credentials.from_service_account_info(info, scopes=SHEETS_SCOPES)

    if file_path:
        return service_account.Credentials.from_service_account_file(file_path, scopes=SHEETS_SCOPES)

    raise ValueError('Google Sheets credentials are not configured')


def _ensure_sheet_tab(service, spreadsheet_id: str, sheet_name: str) -> None:
    meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    tabs = {s['properties']['title'] for s in meta.get('sheets', [])}
    if sheet_name in tabs:
        return
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            'requests': [
                {
                    'addSheet': {
                        'properties': {
                            'title': sheet_name,
                        }
                    }
                }
            ]
        },
    ).execute()


def _build_export_rows(rows):
    header = [
        'id', 'person_name', 'category', 'question', 'created_at',
        'lower_number', 'upper_number', 'changing_line',
        'honke_meaning', 'shike_meaning', 'hexagram_summary',
        'honke_name', 'shike_name', 'ai_response', 'ai_response_short',
        'feedback', 'self_score', 'evaluated_at'
    ]
    values = [header]

    for row in rows:
        line_names = get_line_names()
        honke = get_hexagram(row['lower_number'], row['upper_number'])
        shike = get_changing_hexagram(row['lower_number'], row['upper_number'], row['changing_line'])
        summary = f"本卦:{honke['name']}（{honke['meaning']}） / 之卦:{shike['name']}（{shike['meaning']}） / 変爻:{line_names[row['changing_line']]}"
        values.append([
            _csv_safe(row['id']),
            _csv_safe(row['person_name']),
            _csv_safe(row['category']),
            _csv_safe(row['question']),
            _csv_safe(row['created_at']),
            row['lower_number'],
            row['upper_number'],
            row['changing_line'],
            _csv_safe(honke['meaning']),
            _csv_safe(shike['meaning']),
            _csv_safe(summary),
            _csv_safe(row['honke_name']),
            _csv_safe(row['shike_name']),
            _csv_safe(row['ai_response']),
            _csv_safe(_summarize_ai_response(row['ai_response'])),
            _csv_safe(row['feedback']),
            row['self_score'] if row['self_score'] is not None else '',
            _csv_safe(row['evaluated_at']),
        ])

    return values


def _infer_frontend_dev_server() -> str:
    """FRONTEND_DEV_SERVER 未設定時にアクセス元から推定する。"""
    host = request.host
    scheme = request.headers.get("X-Forwarded-Proto", request.scheme)

    # Codespaces: <name>-5000.app.github.dev -> <name>-5173.app.github.dev
    if re.search(r"-\d+\.app\.github\.dev$", host):
        inferred_host = re.sub(r"-\d+\.app\.github\.dev$", "-5173.app.github.dev", host)
        return f"{scheme}://{inferred_host}"

    return "http://127.0.0.1:5173"


# ─── フロントエンド配信 ───────────────────────────────────────────

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """ビルド済みの React アプリを配信する。"""
    index_file = os.path.join(FRONTEND_DIST, 'index.html')
    if not os.path.exists(index_file):
        # dist 未生成時は Vite 開発サーバーへ逃がして 404 を防ぐ
        dev_server = os.environ.get('FRONTEND_DEV_SERVER') or _infer_frontend_dev_server()
        if path:
            return redirect(f"{dev_server.rstrip('/')}/{path}")
        return redirect(dev_server)

    target = os.path.join(FRONTEND_DIST, path)
    if path and os.path.exists(target):
        return send_from_directory(FRONTEND_DIST, path)
    return send_from_directory(FRONTEND_DIST, 'index.html')


# ─── API エンドポイント ───────────────────────────────────────────

@app.route("/api/divine", methods=["POST"])
def divine():
    """占いを実行し、本卦・変爻・之卦を返す。

    Returns:
        JSON:
            - lower_number: 下卦番号 (1-8)
            - upper_number: 上卦番号 (1-8)
            - changing_line: 変爻の位置 (1-6)
            - honke: 本卦データ
            - shike: 之卦データ
    """
    payload = request.get_json(silent=True) or {}
    person_name = (payload.get('person_name') or '匿名').strip()
    question = (payload.get('question') or '（未入力）').strip()
    category = (payload.get('concern_type') or '').strip() or _infer_category_from_question(question)

    lower_number = random.randint(1, 8)
    upper_number = random.randint(1, 8)
    changing_line = random.randint(1, 6)

    honke = get_hexagram(lower_number, upper_number)
    shike = get_changing_hexagram(lower_number, upper_number, changing_line)
    line_names = get_line_names()
    changing_line_name = line_names[changing_line]

    ai_response = generate_gemini_response(
        person_name=person_name,
        question=question,
        honke=honke,
        shike=shike,
        changing_line=changing_line,
        changing_line_name=changing_line_name,
    )

    created_at = datetime.now().isoformat(timespec='seconds')
    with get_db_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO divinations (
                person_name, question, created_at,
                lower_number, upper_number, changing_line,
                honke_name, shike_name, category, ai_response, feedback, self_score, evaluated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                person_name,
                question,
                created_at,
                lower_number,
                upper_number,
                changing_line,
                honke['name'],
                shike['name'],
                category,
                ai_response,
                '',
                None,
                None,
            ),
        )
        conn.commit()
        divination_id = cursor.lastrowid

    return jsonify({
        "id": divination_id,
        "person_name": person_name,
        "question": question,
        "category": category,
        "created_at": created_at,
        "lower_number": lower_number,
        "upper_number": upper_number,
        "changing_line": changing_line,
        "changing_line_name": changing_line_name,
        "honke": honke,
        "shike": shike,
        "ai_response": ai_response,
        "feedback": "",
        "self_score": None,
        "evaluated_at": None,
        "hexagram_summary": f"本卦:{honke['name']}（{honke['meaning']}） / 之卦:{shike['name']}（{shike['meaning']}） / 変爻:{changing_line_name}",
    })


@app.route("/api/trigrams", methods=["GET"])
def trigrams():
    """八卦の一覧を返す。"""
    return jsonify(TRIGRAMS)


@app.route("/api/health", methods=["GET"])
def health():
    """ヘルスチェック用エンドポイント。"""
    return jsonify({"status": "ok"})


@app.route("/api/divinations", methods=["GET"])
def list_divinations():
    """保存済み占い履歴を新しい順で返す。"""
    where_clause, params = _build_divinations_filters(request.args)

    with get_db_connection() as conn:
        rows = conn.execute(
            f"""
            SELECT id, person_name, question, created_at,
                     category,
                   lower_number, upper_number, changing_line,
                     honke_name, shike_name, ai_response, feedback, self_score, evaluated_at
            FROM divinations
            {where_clause}
            ORDER BY datetime(created_at) DESC, id DESC
            """
            , params
        ).fetchall()
    return jsonify([serialize_divination_row(r) for r in rows])


@app.route("/api/divinations/export.csv", methods=["GET"])
def export_divinations_csv():
    """検索条件に一致する履歴を CSV で返す。"""
    where_clause, params = _build_divinations_filters(request.args)

    with get_db_connection() as conn:
        rows = conn.execute(
            f"""
            SELECT id, person_name, question, created_at,
                     category,
                   lower_number, upper_number, changing_line,
                     honke_name, shike_name, ai_response, feedback, self_score, evaluated_at
            FROM divinations
            {where_clause}
            ORDER BY datetime(created_at) DESC, id DESC
            """,
            params,
        ).fetchall()

    output = StringIO()
    writer = csv.writer(output)
    values = _build_export_rows(rows)
    for row in values:
        writer.writerow(row)

    # UTF-8 BOM を付け、Mac/Google Sheets での日本語読込互換性を上げる
    csv_text = '\ufeff' + output.getvalue()
    filename = f"divinations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return Response(
        csv_text,
        mimetype='text/csv; charset=utf-8',
        headers={
            'Content-Disposition': f'attachment; filename={filename}'
        }
    )


@app.route('/api/divinations/stats/trend', methods=['GET'])
def divinations_score_trend():
    """評価日時ベースで一致度推移を返す。group=weekly|monthly"""
    group = (request.args.get('group') or 'weekly').strip().lower()
    if group not in {'weekly', 'monthly'}:
        return jsonify({'error': 'group must be weekly or monthly'}), 400

    where_clause, params = _build_divinations_filters(request.args)
    if where_clause:
        where_clause = where_clause + ' AND self_score IS NOT NULL AND evaluated_at IS NOT NULL'
    else:
        where_clause = 'WHERE self_score IS NOT NULL AND evaluated_at IS NOT NULL'

    if group == 'weekly':
        period_expr = "strftime('%Y-W%W', evaluated_at)"
    else:
        period_expr = "strftime('%Y-%m', evaluated_at)"

    with get_db_connection() as conn:
        rows = conn.execute(
            f"""
            SELECT
                {period_expr} AS period,
                COUNT(*) AS evaluated_count,
                ROUND(AVG(self_score), 3) AS avg_score,
                MIN(self_score) AS min_score,
                MAX(self_score) AS max_score
            FROM divinations
            {where_clause}
            GROUP BY period
            ORDER BY period ASC
            """,
            params,
        ).fetchall()

    return jsonify([
        {
            'period': r['period'],
            'evaluated_count': r['evaluated_count'],
            'avg_score': r['avg_score'],
            'min_score': r['min_score'],
            'max_score': r['max_score'],
        }
        for r in rows
    ])


@app.route('/api/divinations/stats/categories', methods=['GET'])
def divinations_score_by_category():
    """カテゴリ別の一致度比較を返す。"""
    where_clause, params = _build_divinations_filters(request.args)
    if where_clause:
        where_clause = where_clause + ' AND self_score IS NOT NULL'
    else:
        where_clause = 'WHERE self_score IS NOT NULL'

    with get_db_connection() as conn:
        rows = conn.execute(
            f"""
            SELECT
                category,
                COUNT(*) AS evaluated_count,
                ROUND(AVG(self_score), 3) AS avg_score,
                MIN(self_score) AS min_score,
                MAX(self_score) AS max_score
            FROM divinations
            {where_clause}
            GROUP BY category
            ORDER BY avg_score DESC, evaluated_count DESC
            """,
            params,
        ).fetchall()

    return jsonify([
        {
            'category': r['category'] or '総合',
            'evaluated_count': r['evaluated_count'],
            'avg_score': r['avg_score'],
            'min_score': r['min_score'],
            'max_score': r['max_score'],
        }
        for r in rows
    ])


@app.route('/api/divinations/export/sheets', methods=['POST'])
def export_divinations_to_sheets():
    """検索条件に一致した履歴を Google スプレッドシートへワンクリック転送。"""
    payload = request.get_json(silent=True) or {}
    filters = payload.get('filters') or {}
    sheet_name = (payload.get('sheet_name') or os.environ.get('GOOGLE_SHEETS_TAB_NAME') or 'Divinations').strip()
    spreadsheet_id = (payload.get('spreadsheet_id') or os.environ.get('GOOGLE_SHEETS_SPREADSHEET_ID') or '').strip()

    if not spreadsheet_id:
        return jsonify({'error': 'spreadsheet_id is required'}), 400

    class _Args:
        def __init__(self, data):
            self.data = data
        def get(self, key):
            return self.data.get(key)

    where_clause, params = _build_divinations_filters(_Args(filters))

    with get_db_connection() as conn:
        rows = conn.execute(
            f"""
            SELECT id, person_name, question, created_at,
                     category,
                   lower_number, upper_number, changing_line,
                   honke_name, shike_name, ai_response, feedback, self_score, evaluated_at
            FROM divinations
            {where_clause}
            ORDER BY datetime(created_at) DESC, id DESC
            """,
            params,
        ).fetchall()

    values = _build_export_rows(rows)

    try:
        creds = _get_google_creds()
        service = build('sheets', 'v4', credentials=creds, cache_discovery=False)
        _ensure_sheet_tab(service, spreadsheet_id, sheet_name)

        service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range=f'{sheet_name}!A:Z',
            body={},
        ).execute()

        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=f'{sheet_name}!A1',
            valueInputOption='RAW',
            body={'values': values},
        ).execute()
    except (ValueError, json.JSONDecodeError) as exc:
        return jsonify({'error': str(exc)}), 400
    except HttpError as exc:
        return jsonify({'error': f'Google Sheets API error: {exc}'}), 502

    return jsonify({
        'ok': True,
        'spreadsheet_id': spreadsheet_id,
        'sheet_name': sheet_name,
        'row_count': max(len(values) - 1, 0),
    })


@app.route("/api/divinations/<int:divination_id>", methods=["PATCH"])
def update_divination_feedback(divination_id: int):
    """履歴のフィードバック欄を更新する。"""
    payload = request.get_json(silent=True) or {}
    feedback = payload.get('feedback')
    self_score_raw = payload.get('self_score')
    evaluate_requested = False

    updates = []
    params = []

    if feedback is not None:
        updates.append("feedback = ?")
        params.append(str(feedback).strip())
        evaluate_requested = True

    if self_score_raw is not None:
        if self_score_raw == '':
            updates.append("self_score = NULL")
        else:
            try:
                self_score = int(self_score_raw)
            except (TypeError, ValueError):
                return jsonify({"error": "self_score must be 1-5"}), 400
            if not 1 <= self_score <= 5:
                return jsonify({"error": "self_score must be 1-5"}), 400
            updates.append("self_score = ?")
            params.append(self_score)
        evaluate_requested = True

    if evaluate_requested:
        updates.append("evaluated_at = ?")
        params.append(datetime.now().isoformat(timespec='seconds'))

    if not updates:
        return jsonify({"error": "no fields to update"}), 400

    with get_db_connection() as conn:
        cursor = conn.execute(
            f"UPDATE divinations SET {', '.join(updates)} WHERE id = ?",
            params + [divination_id],
        )
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "not found"}), 404

        row = conn.execute(
            """
            SELECT id, person_name, question, created_at,
                     category,
                   lower_number, upper_number, changing_line,
                     honke_name, shike_name, ai_response, feedback, self_score, evaluated_at
            FROM divinations
            WHERE id = ?
            """,
            (divination_id,),
        ).fetchone()

    return jsonify(serialize_divination_row(row))


# ─── 【AI鑑定エンドポイント】命盤データからClaude APIで鑑定文を生成 ───

@app.route("/api/divination/ai-reading", methods=["POST"])
def ai_reading():
    """
    生年月日から四柱推命命盤を生成し、Claude APIで鑑定文を生成
    
    APIキーが未設定の場合はモックデータを返し、API課金を防止
    
    Request body:
    {
        "natal_chart": {
            "year": 1990,
            "month": 5,
            "day": 15,
            "hour": 14 or null,
            "gender": "男" or "女" or "不明"
        },
        "user_query": "今年の運勢は？",
        "use_mock": false
    }
    
    Response:
    {
        "status": "success" or "error",
        "divination": "鑑定文（300文字程度）",
        "mode": "api" or "mock",
        "model": "claude-3-5-sonnet-20241022" or "mock-...",
        "hour_pillar_mode": "4柱" or "3柱",
        "message": "ステータスメッセージ"
    }
    """
    try:
        payload = request.get_json(silent=True) or {}
        
        natal_chart_input = payload.get("natal_chart")
        user_query = payload.get("user_query")
        use_mock = payload.get("use_mock", False)
        
        # バリデーション
        if not natal_chart_input:
            return jsonify({
                "status": "error",
                "error_type": "validation_error",
                "message": "natal_chart は必須です"
            }), 400
        
        if not user_query:
            return jsonify({
                "status": "error",
                "error_type": "validation_error",
                "message": "user_query は必須です"
            }), 400
        
        # 入力パラメータの取得
        year = natal_chart_input.get("year")
        month = natal_chart_input.get("month")
        day = natal_chart_input.get("day")
        hour = natal_chart_input.get("hour")
        gender = natal_chart_input.get("gender", "不明")
        
        if not all([year, month, day]):
            return jsonify({
                "status": "error",
                "error_type": "validation_error",
                "message": "年月日は必須です"
            }), 400
        
        # 【新規】干支計算ロジック（簡易版）
        # fortune-core がある場合はそちらを使用、なければ簡易計算
        try:
            # 試試：fortune-core から干支計算を行う
            # （実装がない場合は ImportError でキャッチし、簡易版を使用）
            try:
                # fortune-core への相対インポートを試みる
                import sys
                from pathlib import Path
                fortune_core_path = Path(__file__).parent.parent / 'fortune-core' / 'src'
                if fortune_core_path.exists():
                    sys.path.insert(0, str(fortune_core_path))
                
                # 干支計算関数（存在しない可能性が高いので、一度確認）
                from fortune_core_stem_branch import calculate_stems_branches as calc_sb
                stems_branches = calc_sb(year, month, day, hour)
                
            except (ImportError, AttributeError):
                # fortune-core が利用不可の場合は簡易版を使用
                # 簡易的な干支マッピング（1960年開始で甲子からのサイクル）
                STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
                BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
                
                # 年柱の計算（1960年 = 甲子 とする）
                year_offset = (year - 1960) % 60
                year_stem = STEMS[year_offset % 10]
                year_branch = BRANCHES[year_offset % 12]
                year_pillar = year_stem + year_branch
                
                # 月柱の計算（簡易版：正確な節気判定は fortune-core に委譲）
                month_offset = (month - 1) % 12
                month_stem = STEMS[(year_offset + month) % 10]
                month_branch = BRANCHES[month_offset]
                month_pillar = month_stem + month_branch
                
                # 日柱の計算（簡易版）
                day_stem = STEMS[(year_offset + day) % 10]
                day_branch = BRANCHES[(day - 1) % 12]
                day_pillar = day_stem + day_branch
                
                # 時柱の計算
                hour_pillar = None
                if hour is not None:
                    hour_branch = BRANCHES[(hour // 2) % 12]
                    hour_stem = STEMS[(year_offset + hour) % 10]
                    hour_pillar = hour_stem + hour_branch
                
                stems_branches = {
                    "year_pillar": year_pillar,
                    "month_pillar": month_pillar,
                    "day_pillar": day_pillar,
                    "hour_pillar": hour_pillar
                }
            
            # 干支オブジェクトに変換
            natal_chart = {
                "year_pillar": stems_branches.get("year_pillar"),
                "month_pillar": stems_branches.get("month_pillar"),
                "day_pillar": stems_branches.get("day_pillar"),
                "hour_pillar": stems_branches.get("hour_pillar"),
                "gender": gender
            }
        
        except Exception as e:
            return jsonify({
                "status": "error",
                "error_type": "calculation_error",
                "message": f"干支計算エラー: {str(e)}"
            }), 400
        
        # AI鑑定サービスが初期化されているか確認
        if not divination_service:
            return jsonify({
                "status": "error",
                "error_type": "service_error",
                "message": "AI鑑定サービスが利用不可です"
            }), 503
        
        # 鑑定文を生成（モックor実API）
        result = divination_service.generate_divination(
            natal_chart=natal_chart,
            user_query=user_query,
            use_mock=use_mock
        )
        
        # ステータスコードを結果に応じて選択
        status_code = 200 if result.get("status") == "success" else 400
        
        return jsonify(result), status_code
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "error_type": "internal_error",
            "message": f"予期しないエラー: {str(e)}"
        }), 500
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "error_type": "internal_error",
            "message": f"予期しないエラー: {str(e)}"
        }), 500


@app.route("/api/divination/status", methods=["GET"])
def ai_reading_status():
    """
    AI鑑定サービスの状態を確認（デバッグ用）
    
    APIキーの設定状況やモード（mock/api）を確認できる
    
    Response:
    {
        "has_api_key": true or false,
        "mode": "api" or "mock",
        "message": "ステータスメッセージ"
    }
    """
    if not divination_service:
        return jsonify({
            "status": "error",
            "message": "AI鑑定サービスが初期化されていません"
        }), 503
    
    status = divination_service.get_status()
    return jsonify(status), 200


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    port = int(os.environ.get("PORT", "5000"))
    app.run(debug=debug, host="0.0.0.0", port=port)


init_db()
