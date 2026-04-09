# 🔍 Game Glitch Investigator: Applied AI System

## 📌 Base Project
This project extends **Module 1: Game Glitch Investigator** — a Streamlit number guessing game full of intentional bugs. The original project focused on identifying and fixing AI-generated code using VS Code Copilot. The base app included a broken scoring system, misleading hints, and state management bugs that had to be diagnosed and repaired.

This extended version evolves that prototype into a full applied AI system with two new components: a **RAG-powered bug pattern lookup** and an **automated reliability evaluator**.

---

## 🧠 What This Project Does

The Game Glitch Investigator is a three-tab Streamlit app:

| Tab | Description |
|-----|-------------|
| 🎮 Glitchy Guesser | The original fixed number guessing game |
| 📚 Bug Pattern Lookup | RAG system that retrieves relevant bug docs from a local knowledge base |
| 🧪 Reliability Evaluator | Automated test harness that runs 7 checks on game logic and the retriever |

---

## 🏗️ Architecture Overview

```
User Input (bug description or keyword)
        ↓
  retriever.py — keyword search over /knowledge_base/ .md files
        ↓
  Relevant docs returned (bug patterns, error types)
        ↓
  Streamlit UI displays matched documentation
        ↓
  Reliability Evaluator runs automated checks on retriever + game logic
```

The system uses **Retrieval-Augmented Generation (RAG)** without an external AI API — the retriever searches a local knowledge base of markdown files covering common Python bug patterns and error types. Results are surfaced directly to the user.

The knowledge base is split into two categories:
- `knowledge_base/bug_patterns/` — infinite loops, off-by-one errors, wrong comparisons
- `knowledge_base/error_types/` — IndexError, TypeError, NameError

---

## ⚙️ Setup Instructions

1. Clone the repo:
   ```bash
   git clone https://github.com/stevenGGG23/applied-ai-system-project.git
   cd applied-ai-system-project
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

No API key required.

---

## 💬 Sample Interactions

### Bug Pattern Lookup
**Input:** `my while loop never stops running`
**Retrieved docs:** `infinite_loop`, `off_by_one`
The retriever matches keywords like "loop" and "running" against knowledge base content and returns the most relevant pattern docs.

**Input:** `list index out of range`
**Retrieved docs:** `index_error`, `off_by_one`

**Input:** `cannot compare str and int`
**Retrieved docs:** `type_error`, `wrong_comparison`

### Reliability Evaluator
Clicking **Run All Tests** runs 7 automated checks:
- `check_guess` returns correct outcomes for win/too high/too low
- `parse_guess` accepts valid input and rejects out-of-range values
- Retriever returns docs for known keywords and no docs for gibberish

---

## 🔧 Design Decisions

- **No external API** — the RAG system uses local markdown files instead of a vector database or LLM. This makes the app fully self-contained, reproducible, and free to run.
- **Keyword matching over embeddings** — simple set intersection scoring is transparent and easy to test. A future version could swap in sentence embeddings for better semantic retrieval.
- **Knowledge base as markdown** — plain `.md` files are easy to read, edit, and extend without any database setup.
- **Reliability evaluator in the UI** — running tests inside Streamlit makes the evaluation visible and easy to demo without needing a separate test runner.

---

## 🧪 Testing Summary

7/7 automated tests pass covering game logic (`check_guess`, `parse_guess`) and the RAG retriever. The retriever correctly matches known bug keywords and correctly returns nothing for gibberish input. One limitation: keyword matching misses synonyms — searching "endless loop" won't match the infinite loop doc since the word "infinite" isn't present in the query.

---

## 🪞 Reflection

This project taught me how RAG works at a fundamental level — retrieval doesn't have to mean embeddings and vector databases. Even simple keyword overlap can surface useful context if the knowledge base is well-structured. Building the reliability evaluator also showed how important it is to test the retrieval layer separately from the generation layer, since a broken retriever would silently degrade output quality without an obvious error.

---

## 🎥 Demo Walkthrough

> Loom video link here (add before submission)

---

## 🐛 Original Bugs Fixed (Module 1)

| # | File | Bug | Fix |
|---|------|-----|-----|
| 1 | `app.py` | Secret number re-rolled on every rerun | Guarded state init with `if key not in st.session_state` |
| 2 | `app.py` | New Game didn't clear guess history | Added `st.session_state.history = []` to New Game handler |
| 3 | `app.py` | Invalid guesses consumed an attempt | Refunded attempt counter on parse error |
| 4 | `logic_utils.py` | Hard range was 1–50 (easier than Normal) | Changed Hard range to 1–200 |
| 5 | `logic_utils.py` | Too High on even attempts gave +5 points | All wrong guesses now deduct flat 5 points |
| 6 | `logic_utils.py` | Misleading FIXME comment | Removed stale comment |

---

## 📸 Screenshots

![App Screenshot](assets/screenshot.png)

---

## Difficulty Reference

| Difficulty | Range | Attempts |
|------------|-------|----------|
| Easy | 1 – 20 | 10 |
| Normal | 1 – 100 | 7 |
| Hard | 1 – 200 | 5 |