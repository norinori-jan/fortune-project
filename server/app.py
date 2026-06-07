"""
Flask API Server for Tarot Fortune Reading
"""
import os
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

load_dotenv()

FORTUNE_PROJECT_ROOT = Path(__file__).parent.parent
TAROT_REGISTRY_PATH = FORTUNE_PROJECT_ROOT / "fortune-registry" / "tarot"
REGISTRY_FILE = FORTUNE_PROJECT_ROOT / "core" / "registry_a.json"

sys.path.insert(0, str(TAROT_REGISTRY_PATH))

try:
    from tarot_engine import TarotEngine, SpreadType
    from tarot_registry_bridge import TarotRegistryBridge
except ImportError as e:
    print(f"Warning: Could not import tarot modules: {e}")

app = Flask(__name__)
CORS(app)

TAROT_DIR = os.path.join(os.path.dirname(__file__), '..', 'fortune-registry', 'tarot')

@app.route('/')
def index():
    return send_from_directory(TAROT_DIR, 'index.html', mimetype='text/html')

@app.route('/manifest.json')
def manifest():
    return send_from_directory(TAROT_DIR, 'manifest.json')

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory(TAROT_DIR, 'service-worker.js')

@app.route('/icon-192.png')
def icon192():
    return send_from_directory(TAROT_DIR, 'icon-192.png')

@app.route('/icon-512.png')
def icon512():
    return send_from_directory(TAROT_DIR, 'icon-512.png')

@app.route('/tarot/<path:filename>')
def tarot_static(filename):
    return send_from_directory(TAROT_DIR, filename)

API_KEYS = {
    "gemini": os.getenv("GEMINI_API_KEY", ""),
    "openai": os.getenv("OPENAI_API_KEY", ""),
    "claude": os.getenv("CLAUDE_API_KEY", ""),
}

bridge = None
try:
    MAJOR_JSON_PATH = TAROT_REGISTRY_PATH / "major.json"
    if MAJOR_JSON_PATH.exists():
        bridge = TarotRegistryBridge(str(MAJOR_JSON_PATH))
    else:
        print(f"Warning: major.json not found at {MAJOR_JSON_PATH}")
except Exception as e:
    print(f"Error initializing TarotRegistryBridge: {e}")

def load_registry() -> dict:
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"tarot": []}

def save_registry(registry: dict):
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)

def append_tarot_entry(entry: dict):
    registry = load_registry()
    if "tarot" not in registry:
        registry["tarot"] = []
    registry["tarot"].append(entry)
    save_registry(registry)

SYSTEM_PROMPT = """あなたは神秘的で洞察力のあるタロット占い師「叡智の声」です。以下のルールで占いの解読を行ってください。
- 日本語で、詩的かつ親しみやすい文体で語りかけてください
- 各カードの意味を統合し、全体的なメッセージとして伝えてください
- スプレッドの文脈（位置の意味）を必ず考慮してください
- 五行（木火土金水）の観点も織り交ぜてください
- 300～400文字程度でまとめてください
- 最後に一言、励ましや行動のヒントを添えてください"""

def call_claude(prompt: str) -> tuple[bool, str]:
    if not API_KEYS["claude"]:
        return False, "Claude API key not configured"
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type": "application/json", "x-api-key": API_KEYS["claude"], "anthropic-version": "2023-06-01"},
            json={"model": "claude-sonnet-4-20250514", "max_tokens": 1000, "system": SYSTEM_PROMPT, "messages": [{"role": "user", "content": prompt}]},
        )
        if response.status_code != 200:
            return False, f"Claude API Error: {response.status_code}"
        return True, response.json()["content"][0]["text"]
    except Exception as e:
        return False, str(e)

def call_gemini(prompt: str) -> tuple[bool, str]:
    if not API_KEYS["gemini"]:
        return False, "Gemini API key not configured"
    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEYS['gemini']}",
            headers={"Content-Type": "application/json"},
            json={"system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]}, "contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"maxOutputTokens": 8192}},
        )
        if response.status_code != 200:
            return False, f"Gemini API Error: {response.status_code}"
        return True, response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return False, str(e)

def call_openai(prompt: str) -> tuple[bool, str]:
    if not API_KEYS["openai"]:
        return False, "OpenAI API key not configured"
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEYS['openai']}"},
            json={"model": "gpt-4o", "max_tokens": 1000, "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]},
        )
        if response.status_code != 200:
            return False, f"OpenAI API Error: {response.status_code}"
        return True, response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return False, str(e)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat(), "tarot_available": bridge is not None})

@app.route("/api/tarot/draw", methods=["POST"])
def draw_tarot():
    if not bridge:
        return jsonify({"success": False, "error": "Tarot engine not available"}), 500
    try:
        body = request.get_json()
        spread_type_str = body.get("spread_type", "one_oracle")
        question = body.get("question", "")
        # フロントエンドのスプレッド名をSpreadTypeに変換
        spread_map = {
            "one": "one_oracle",
            "three": "three_card",
            "yesno": "yes_no",
            "daily": "daily",
            "celtic": "celtic_mini",
        }
        spread_type_str = spread_map.get(spread_type_str, spread_type_str)
        spread_type = SpreadType[spread_type_str.upper()] if spread_type_str.upper() in SpreadType.__members__ else SpreadType.ONE_ORACLE
        result = bridge.execute_and_export(spread_type, question)
        append_tarot_entry(result)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/tarot/interpret", methods=["POST"])
def interpret_tarot():
    try:
        body = request.get_json()
        cards_context = body.get("cards_context", "")
        ais = body.get("ais", ["gemini", "openai"])
        if not cards_context:
            return jsonify({"success": False, "error": "cards_context required"}), 400
        interpretations = {}
        if "claude" in ais:
            success, text = call_claude(cards_context)
            interpretations["claude"] = {"success": success, "text": text}
        if "gemini" in ais:
            success, text = call_gemini(cards_context)
            interpretations["gemini"] = {"success": success, "text": text}
        if "openai" in ais:
            success, text = call_openai(cards_context)
            interpretations["openai"] = {"success": success, "text": text}
        return jsonify({"success": True, "interpretations": interpretations})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/registry/tarot", methods=["GET"])
def get_tarot_history():
    try:
        registry = load_registry()
        return jsonify({"success": True, "count": len(registry.get("tarot", [])), "entries": registry.get("tarot", [])})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route("/api/config", methods=["GET"])
def get_config():
    return jsonify({
        "api_keys": {k: "configured" if v else "not configured" for k, v in API_KEYS.items()},
        "registry_file": str(REGISTRY_FILE),
        "tarot_registry_path": str(TAROT_REGISTRY_PATH),
    })

@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "error": "Not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"success": False, "error": "Internal server error"}), 500

if __name__ == "__main__":
    print(f"Tarot Fortune Server Starting...")
    app.run(debug=True, host="0.0.0.0", port=5000)
