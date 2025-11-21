🚀 Impact Analyzer MVP — AI-Powered Code Change Impact Tool
Impact Analyzer is an intelligent, automated tool that analyzes code changes across complex applications and tells you what will break, what modules are impacted, what the risk level is, and what tests you should run.
It combines:


🧠 Static code analysis


🔗 Dependency graph analysis


🤖 Gemini AI to enrich impact summaries


🔍 GitHub PR bot to comment automatically on pull requests


🌐 Frontend UI to paste diffs and visualize results



📦 Project Overview
This project detects:


Which files changed


Which modules depend on those files


What impact the change creates


How risky the change is


Recommended test cases


AI-generated descriptions, summaries & risks


Designed for:


Large distributed codebases


Microservices


Multi-module applications


CI-CD pipelines


GitHub PR automation



🏗️ Architecture
                        ┌────────────────────────────┐
                        │        FRONTEND (React)     │
                        │  - Diff input box           │
                        │  - Results dashboard        │
                        └───────────────┬────────────┘
                                        │ REST / JSON
                                        ▼
                    ┌────────────────────────────────────────┐
                    │      BACKEND API (Flask, Python)       │
                    │ /analyze                                │
                    └─────────────────┬──────────────────────┘
                                      │
        ┌─────────────────────────────┼────────────────────────────┐
        │                             │                            │
        ▼                             ▼                            ▼
┌────────────────┐       ┌──────────────────────┐       ┌─────────────────────┐
│ Static Analyzer │       │ Dependency Analyzer  │       │ Gemini AI Enricher  │
│ - Extract files │       │ - Map to modules     │       │ - Summary           │
│ - Parse diff    │──────►│ - Risk evaluation    │──────►│ - Suggested tests   │
└────────────────┘       └──────────────────────┘       └─────────────────────┘
                                        │
                                        ▼
                     ┌─────────────────────────────┐
                     │      JSON API Response       │
                     └─────────────────────────────┘


🧠 How it Works (Simple Explanation)
1️⃣ You paste a Git diff into the app
2️⃣ Backend extracts changed files
3️⃣ It maps files → modules (via dependency graph)
4️⃣ Risk engine assigns probability of breaking
5️⃣ Gemini AI enriches the result:


human-readable summary


risk justification


suggested tests


inferred impact


6️⃣ You get a clean report.

⚙️ How it Works (Technical Pipeline)
1. Diff Parsing
static_analysis.py extracts all file paths from:


diff --git lines


+++ b/... markers


fallback regex for file extensions


2. Dependency Graph Mapping
graph/dependency_graph.py loads:
repository_map.json

Which defines:


modules


file → module mapping


module → downstream dependencies


3. Impact Engine
impact_engine.py:


Calculates direct impacts


Traverses dependency graph


Scores impact level


Produces deterministic analysis


4. AI Integration
ai_engine.py:


Creates compact JSON prompt


Sends to Gemini (google-genai SDK)


Parses structured JSON output


Merges AI summaries + tests + risk


5. API Returns
changed_files
impacted_modules
overall_risk
ai_summary
ai_suggested_tests
ai_risk


🔧 Requirements
📌 Backend (Python)
Create a virtual environment:
python -m venv .venv
.\.venv\Scripts\activate   # Windows
source .venv/bin/activate # Mac/Linux

Install dependencies:
pip install -r requirements.txt

Dependencies include:


Flask


networkx


python-dotenv


google-genai


requests / axios (frontend)


React + Vite + Tailwind UI



▶️ Running the Backend (Local)
From root of repo:
cd backend
.\.venv\Scripts\activate
pip install -r requirements.txt
python app.py

Backend runs at:
http://localhost:8000

Test:
POST /analyze


🎨 Running the Frontend
cd frontend
npm install
npm run dev

App runs at:
http://localhost:5173

Configure frontend to point to backend:
VITE_API_URL=http://localhost:8000


You can visit the site following this hyperlink : https://impact-analyser-mvp-expanded.vercel.app/

☁️ Deploying on Render
1. Backend:


Create Web Service


Root directory: backend


Auto-detects Dockerfile


Add environment variable:


GEMINI_API_KEY=<your_key>
GEMINI_MODEL=gemini-1.5-flash


🤖 GitHub PR Impact Bot
Create:
.github/workflows/pr-impact-bot.yml

Bot will:


Extract PR diff


Call backend


Post comment automatically


Include risk, summary, impacted modules



🌟 Features
✔ Static Diff Analyzer
✔ Dependency Traversal
✔ Module Risk Evaluator
✔ Gemini AI Integration
✔ PR Automation
✔ Full React Frontend
✔ Clean API
