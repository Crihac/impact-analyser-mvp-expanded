from flask import Flask, request, jsonify
from analyzer.static_analysis import parse_changed_files
from analyzer.impact_engine import analyze_impact
from utils.repo_map_loader import load_repo_map_if_exists
import os

app = Flask(__name__)

# Load optional repository_map.json
REPO_MAP = load_repo_map_if_exists(os.path.join(os.path.dirname(__file__), "..", "repository_map.json"))

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json() or {}
    diff = data.get("diff", "")
    repo_map_override = data.get("repo_map")

    # Step 1: Extract changed files
    files = parse_changed_files(diff)

    # Step 2: Run impact analysis
    result = analyze_impact(files, repo_map=repo_map_override or REPO_MAP)
    return jsonify(result), 200

@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Impact Analyzer API running (Python 3.14 compatible!)"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8000)), debug=True)
