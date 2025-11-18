# WriteWise — Essay & Assignment Feedback Tool

**One-line:** A Streamlit-based essay feedback tool using BERT (CoLA) for acceptability checks and T5-small for improvement suggestions.

---

## Contents
- `feedback_tool.py` — Streamlit app (entry point)
- `requirements.txt` — Python dependencies
- `screenshots/` — images showing app UI and outputs
- `demo_script.txt` — short script for the 1–2 minute demo
- `.gitignore` — excludes venv and model caches

---

## Features
- Grammar/style acceptability per sentence (BERT CoLA)
- Improvement suggestions / paraphrase (T5-small)
- Readability metrics and basic structural checks
- Automated grade (basic rubric)
- Streamlit UI with one-click feedback and Reset

---

## Quick setup (local)
1. Clone repository:
```bash
git clone <YOUR_REPO_URL>
cd Essay_Feedback_Tool
