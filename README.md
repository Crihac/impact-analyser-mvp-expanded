# Impact Analyzer MVP (Expanded)

This expanded repository includes:
- A Flask backend compatible with Python 3.14 for environments that require it
- Improved impact engine and repository map support
- Unit tests and GitHub Actions CI
- Dockerfile and docker-compose support (simple)

## Quick start
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python app.py

## Run tests
pip install pytest
pytest -q tests
