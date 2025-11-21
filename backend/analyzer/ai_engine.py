# backend/analyzer/ai_engine.py
import os
import json
from typing import Dict, Any, List

# Try to import google-genai; if not present, we'll return graceful fallbacks
try:
    import google.genai as genai  # google-genai package
except Exception:
    genai = None  # fallback to None so code can still run without the package

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyCOHpHffCNkInfI9G0IcD-Z3GCr1lh1gVU").strip() or None
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
GEMINI_TEMPERATURE = float(os.environ.get("GEMINI_TEMPERATURE", 0.2))

client = None
if GEMINI_API_KEY and genai is not None:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception:
        client = None


def _build_prompt(analysis: Dict[str, Any]) -> str:
    """
    Build a compact prompt that contains changed files, impacted modules and metadata.
    The model will return a JSON-like string describing summary, suggested tests and short reasons.
    """
    changed_files = analysis.get("changed_files", [])
    impacts = analysis.get("impacted_modules", [])
    repo_map = analysis.get("repo_map", {})

    prompt = {
        "task": "Given a set of changed files and impacted modules, provide a concise JSON containing: impacted_modules (module, reason, inferred), suggested_tests (list), risk (Low/Medium/High), summary (short natural language explanation).",
        "changed_files": changed_files,
        "impacts": impacts,
        "repo_map_summary": {k: repo_map.get("module_descriptions", {}).get(k, "") for k in repo_map.get("module_descriptions", {})}
    }

    return json.dumps(prompt, indent=2)


def call_ai_enrich(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """
    Call Gemini to enrich an existing analysis result. If Gemini is unavailable or missing API key,
    return the original analysis with a 'ai_error' flag or a simple fallback summary.
    """
    # If no Gemini client available, return fallback summary
    if not client:
        # Fallback: create a simple summary from the deterministic analysis
        impacts = analysis.get("impacted_modules", [])
        summary_lines: List[str] = []
        for imp in impacts[:5]:
            summary_lines.append(f"{imp.get('module')} (risk {imp.get('risk')}%): {', '.join(imp.get('reasons', []))[:200]}")
        fallback_summary = " | ".join(summary_lines) or "No impacted modules detected."
        analysis["ai_summary"] = fallback_summary
        analysis["ai_provided"] = False
        analysis["ai_error"] = "Gemini client not configured or missing GEMINI_API_KEY"
        return analysis

    prompt = _build_prompt(analysis)

    try:
        # Use the new SDK format - contents is a list with role/parts
        response = client.generate(
            model=GEMINI_MODEL,
            input=prompt,
            temperature=GEMINI_TEMPERATURE,
            max_output_tokens=600,
        )

        text = response.text.strip()
        # Try to interpret model output as JSON — model should be prompted to return JSON
        parsed = None
        try:
            parsed = json.loads(text)
        except Exception:
            # Try to extract JSON substring if model returns explanation + JSON
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1 and end > start:
                try:
                    parsed = json.loads(text[start:end+1])
                except Exception:
                    parsed = None

        if parsed and isinstance(parsed, dict):
            # Merge parsed fields into analysis in safe way
            analysis["ai_provided"] = True
            analysis["ai_raw_text"] = text
            # Expected keys: impacted_modules, suggested_tests, risk, summary
            if "summary" in parsed:
                analysis["ai_summary"] = parsed.get("summary")
            if "suggested_tests" in parsed:
                analysis["ai_suggested_tests"] = parsed.get("suggested_tests")
            if "risk" in parsed:
                analysis["ai_risk"] = parsed.get("risk")
            if "impacted_modules" in parsed:
                # attempt to merge model's impacted modules with deterministic ones
                analysis["ai_impacted_modules"] = parsed.get("impacted_modules")
        else:
            # No structured JSON detected, store raw text under ai_summary
            analysis["ai_provided"] = True
            analysis["ai_raw_text"] = text
            analysis["ai_summary"] = text if text else "No AI text returned."

    except Exception as e:
        analysis["ai_provided"] = False
        analysis["ai_error"] = str(e)
        analysis["ai_summary"] = "AI call failed: " + str(e)

    return analysis
