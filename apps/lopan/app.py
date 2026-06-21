from __future__ import annotations

from typing import Any, Dict, List

from flask import Flask, jsonify, request
from flask_cors import CORS

from core_logic import FortuneEngine
from logic_engine import get_house_gua_info


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

engine = FortuneEngine()


@app.get("/api/health")
def health() -> Any:
    return jsonify({"ok": True})


@app.route("/api/fortune/direction", methods=["GET", "POST"])
def get_direction() -> Any:
    try:
        if request.method == "GET":
            degree_raw = request.args.get("degree")
        else:
            payload: Dict[str, Any] = request.get_json(silent=True) or {}
            degree_raw = payload.get("degree")

        if degree_raw is None:
            return jsonify({"error": "degree は必須です"}), 400

        degree = float(degree_raw)
        result = engine.get_direction_info(degree)
        bazhai = get_house_gua_info(degree)
        return jsonify({"input_degree": degree, "result": result, "bazhai": bazhai})
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:  # pragma: no cover
        return jsonify({"error": f"direction 判定エラー: {error}"}), 500


@app.post("/api/fortune/strength")
def estimate_strength() -> Any:
    try:
        payload: Dict[str, Any] = request.get_json(silent=True) or {}
        zodiac_list_raw = payload.get("zodiac_list")

        if not isinstance(zodiac_list_raw, list) or not zodiac_list_raw:
            return jsonify({"error": "zodiac_list は空でない配列で指定してください"}), 400

        zodiac_list: List[str] = [str(item) for item in zodiac_list_raw]
        strengths = engine.estimate_element_strength(zodiac_list)

        strongest_element = max(strengths, key=strengths.get)
        return jsonify(
            {
                "input": zodiac_list,
                "strengths": strengths,
                "strongest_element": strongest_element,
            }
        )
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception as error:  # pragma: no cover
        return jsonify({"error": f"strength 計算エラー: {error}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)