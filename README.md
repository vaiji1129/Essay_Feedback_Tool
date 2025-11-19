# WriteWise — Essay & Assignment Feedback Tool

## Overview
WriteWise is an NLP-powered essay feedback system built using Streamlit. 
It analyzes sentence acceptability using BERT (CoLA), generates improvement 
suggestions via T5-small, and computes readability, structure, vocabulary 
complexity, and an automated grade. Designed as part of a virtual internship 
project, it provides students with quick writing feedback.

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

## How to use (demo)

1. Paste an essay into the large text area.
2. Click **Get Feedback**.
3. View:
   - **Analysis** (per-sentence labels + confidence)
   - **Suggestion** (T5 paraphrase)
   - **Grade** and diagnostics
4. Click **Reset** to clear.

## Screenshots

All screenshots are in the `screenshots/` folder.

- `screenshots/homepage.png` — App homepage (empty).
- `screenshots/input_sample.png` — Sample essay pasted before feedback.
- `screenshots/output_full_1.png` — Part 1 of feedback output (analysis / suggestions).
- `screenshots/output_full_2.png` — Part 2 of feedback output (continuation, grade).
- `screenshots/reset.png` — After pressing Reset (empty input).

## Notes & Limitations

- Uses BERT (CoLA) for acceptability checks — this model reports sentence acceptability (LABEL_0 / LABEL_1) and is not a full grammar fixer.
- Uses `t5-small` for paraphrasing; outputs may vary and sometimes include non-English tokens. Consider upgrading to `t5-base` for higher-quality suggestions.
- First run downloads large HuggingFace models (hundreds of MB). If you only want to view screenshots, you can skip running the app.
- Do not commit model weights or the `.venv` folder to GitHub.

## Demo Video

A short 1–2 minute demo shows the app running and producing feedback.

**Video link:** *(paste YouTube or Drive link here after upload - `https://youtu.be/your_unlisted_video`)*  

## Prerequisites

Before running this project, ensure you have the following installed:

- **Python 3.10.x** (recommended)
- **pip** package manager
- A modern web browser (to run Streamlit interface)
- Stable internet connection (for first-time model download)

## Quick setup (local)
1. Clone repository:
```bash
git clone https://github.com/vaiji1129/Essay_Feedback_Tool.git
cd Essay_Feedback_Tool
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Run the Streamlit app:
```bash
streamlit run feedback_tool.py
```

## Contact / Author

V.Vaijinath — vaijinath1129@gmail.com 
