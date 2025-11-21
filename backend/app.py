# backend/app.py
from flask import Flask, request, jsonify
from analyzer.static_analysis import parse_changed_files
from analyzer.impact_engine import analyze_impact
from analyzer.ai_engine import call_ai_enrich
from utils.repo_map_loader import load_repo_map_if_exists
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://impact-analyser-mvp-expanded.vercel.app", "http://localhost:5173"]}})
REPO_MAP = load_repo_map_if_exists(os.path.join(os.path.dirname(__file__), "repository_map.json"))

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json() or {}
    diff = data.get("diff", "")
    repo_map_override = data.get("repo_map")

    # Step 1: Extract changed files
    files = parse_changed_files(diff)

    # Step 2: Deterministic impact analysis (existing engine)
    analysis = analyze_impact(files, repo_map=repo_map_override or REPO_MAP)

    # Attach repo_map for context to AI
    analysis["repo_map"] = repo_map_override or REPO_MAP

    # Step 3: Enrich with Gemini AI (if available)
    enriched = call_ai_enrich(analysis)

    # Return the enriched analysis
    return jsonify(enriched), 200


@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Impact Analyzer API running (with optional Gemini AI)"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), debug=True)
