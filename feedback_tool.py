# feedback_tool.py
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForSeq2SeqLM, pipeline
import textstat
import re

# Reset handler (must run before widgets are created)
if "reset" in st.session_state and st.session_state.reset:
    st.session_state["essay_text"] = ""
    st.session_state.reset = False


# ------------------------------------------------------
# Page Config
# ------------------------------------------------------
st.set_page_config(page_title="WriteWise — Essay Feedback Tool", layout="wide")

# ------------------------------------------------------
# Model Loading
# ------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_models():
    models = {}

    # BERT CoLA for Grammar Acceptability
    try:
        bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        bert_model = AutoModelForSequenceClassification.from_pretrained("textattack/bert-base-uncased-CoLA")
        bert_pipeline = pipeline("text-classification", model=bert_model, tokenizer=bert_tokenizer)
        models['bert_pipeline'] = bert_pipeline
    except Exception as e:
        models['bert_pipeline'] = None
        models['bert_error'] = str(e)

    # T5-small for text improvement
    try:
        t5_tokenizer = AutoTokenizer.from_pretrained("t5-small")
        t5_model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
        t5_pipeline = pipeline("text2text-generation", model=t5_model, tokenizer=t5_tokenizer)
        models['t5_pipeline'] = t5_pipeline
    except Exception as e:
        models['t5_pipeline'] = None
        models['t5_error'] = str(e)

    return models

models = load_models()

# ------------------------------------------------------
# Utility Functions
# ------------------------------------------------------
def split_sentences(text):
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
    if not sentences:
        sentences = [s.strip() for s in re.split(r'[\n\.]+', text) if s.strip()]
    return sentences

def analyze_text(text):
    bert_pipe = models.get('bert_pipeline')
    if bert_pipe is None:
        return None, models.get('bert_error', 'BERT pipeline not available.')

    sentences = split_sentences(text)
    results = []
    for sent in sentences:
        try:
            result = bert_pipe(sent[:512])[0]
        except Exception as e:
            result = {"label": "ERROR", "score": 0.0, "error": str(e)}
        results.append({"sentence": sent, "result": result})
    return results, None

def suggest_improvements(text, num_return_sequences=1):
    t5_pipe = models.get('t5_pipeline')
    if t5_pipe is None:
        return None, models.get('t5_error', 'T5 pipeline not available.')

    prompt = f"improve: {text}"
    try:
        outs = t5_pipe(prompt, max_length=512, num_return_sequences=num_return_sequences, num_beams=5)
    except Exception as e:
        return None, str(e)

    suggestions = [o.get('generated_text', '') for o in outs]
    return suggestions, None

def readability_score(text):
    try:
        return textstat.flesch_kincaid_grade(text)
    except Exception:
        return None

def basic_structure_check(text):
    paragraphs = [p for p in re.split(r'\n\s*\n', text) if p.strip()]
    num_paragraphs = len(paragraphs) if paragraphs else 1 if text.strip() else 0
    sentences = split_sentences(text)
    num_sentences = len(sentences)
    return num_paragraphs, num_sentences

def vocabulary_complexity(text):
    words = re.findall(r'\w+', text.lower())
    return len(set(words)), len(words)

# ------------------------------------------------------
# Grading Function
# ------------------------------------------------------
def grade_text(text):
    analysis, _ = analyze_text(text)
    if analysis is None:
        grammar_issues = 0
    else:
        grammar_issues = 0
        for item in analysis:
            lbl = item["result"].get("label", "")
            if lbl.upper().startswith("LABEL_1"):
                grammar_issues += 1
            if lbl.lower() in ("unacceptable", "not_acceptable", "unacceptable_sentence"):
                grammar_issues += 1

    readability = readability_score(text) or 0
    num_paragraphs, num_sentences = basic_structure_check(text)
    unique_words, total_words = vocabulary_complexity(text)
    vocab_complexity = (unique_words / total_words) if total_words > 0 else 0

    grade = "F"
    if grammar_issues < 5 and readability >= 20 and num_paragraphs >= 2 and vocab_complexity > 0.25:
        if total_words >= 250:
            grade = "A"
        elif total_words >= 200:
            grade = "B"
        elif total_words >= 150:
            grade = "C"
        else:
            grade = "D"
    else:
        grade = "D"

    return {
        "grade": grade,
        "grammar_issues_count": grammar_issues,
        "readability": readability,
        "num_paragraphs": num_paragraphs,
        "num_sentences": num_sentences,
        "vocab_complexity": vocab_complexity,
        "unique_words": unique_words,
        "total_words": total_words
    }

# ------------------------------------------------------
# FINAL STREAMLIT UI (Matches Your Screenshots)
# ------------------------------------------------------
st.title("WriteWise: Essay and Assignment Feedback Tool")

text_input = st.text_area(
    "Enter your essay or assignment text here:",
    key="essay_text"
)

if st.button("Get Feedback"):
    if text_input.strip():

        with st.spinner("Analyzing text..."):
            analysis, analysis_error = analyze_text(text_input)
            suggestions, suggestion_error = suggest_improvements(text_input)
            grade_info = grade_text(text_input)

        if grade_info["num_paragraphs"] <= 1:
            st.write("Insufficient paragraph structure.\n\n"
                     "[Paragraph structure refers to the way paragraphs are organized within the text.]")

        st.subheader("Analysis:")
        if analysis is None:
            st.error(f"Error loading BERT model: {analysis_error}")
        else:
            for item in analysis:
                result = item["result"]
                label = result.get("label", "")
                score = result.get("score", "")
                st.write(
                    f"Text: {label}, Confidence: {score}\n\n"
                    "[LABEL_1 = grammatically incorrect]\n"
                    "[LABEL_0 = acceptable sentence]\n"
                    "[Confidence Score shows model certainty]"
                )

        st.subheader("Suggestions for Improvement:")
        if suggestions is None:
            st.error(f"Error loading T5 model: {suggestion_error}")
        else:
            st.write(suggestions[0])

        st.subheader("Grade:")
        st.write(f"Your grade is: {grade_info['grade']}")

    else:
        st.warning("Please enter some text to get feedback.")

if st.button("Reset"):
    st.session_state.reset = True
    st.experimental_rerun()

st.write(
    "This tool provides real-time feedback on your writing. "
    "Enter your text and click 'Get Feedback' to see analysis, suggestions, and grade."
)
