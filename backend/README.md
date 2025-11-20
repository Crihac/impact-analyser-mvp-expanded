# Impact Analyzer Backend (Expanded)

Features added:
- repo_map.json loader
- extended graph with metadata (coverage, criticality, churn)
- better merging of impacted modules and reasons
- simple utils module

## Run locally
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python app.py

## Test example
curl -X POST http://127.0.0.1:8000/analyze -H "Content-Type: application/json" -d '{"diff":"+++ b/utils/crypto.py"}'
