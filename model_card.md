# Model Card: Game Glitch Investigator

## System Overview
The Game Glitch Investigator is a Streamlit app that extends a number guessing game with a RAG-powered bug pattern lookup system and an automated reliability evaluator. The system retrieves relevant documentation from a local knowledge base of common Python bug patterns and error types, then surfaces that documentation directly to the user.

---

## AI Feature: Retrieval-Augmented Generation (RAG)

The core AI feature is a lightweight RAG pipeline implemented in `retriever.py`. When a user describes a bug or pastes code, the system searches a local knowledge base of markdown files using keyword overlap scoring. The top matching documents are returned and displayed to the user.

**Knowledge base sources:**
- `knowledge_base/bug_patterns/` — infinite loops, off-by-one errors, wrong comparison operators
- `knowledge_base/error_types/` — IndexError, TypeError, NameError

**Retrieval method:** Set intersection scoring between query words and document words. No external API or embeddings are used.

---

## Intended Use
- Students learning to debug Python code
- Developers looking up common bug patterns quickly
- Educational demos of how RAG works without an LLM backend

## Out of Scope
- Production debugging of large or complex codebases
- Languages other than Python
- Bug patterns not covered by the knowledge base

---

## Limitations and Biases

- **Vocabulary mismatch** — The retriever uses exact keyword matching, so synonyms won't work. Searching "endless loop" won't match the infinite loop doc because "infinite" isn't in the query.
- **Small knowledge base** — Only 6 documents are included. Real-world bugs are far more varied and the system will return no results for anything outside those 6 patterns.
- **No ranking by relevance quality** — The scoring is based on word count overlap, not semantic meaning. A document with many overlapping common words could rank higher than a more relevant one.
- **English only** — All knowledge base documents are in English and the retriever doesn't handle other languages.

---

## Potential Misuse
- A user could mistake the retrieved documentation for a complete diagnosis of their specific bug. The system surfaces patterns, not solutions — the user still needs to apply judgment.
- The knowledge base could be extended with incorrect or misleading documentation, causing bad results. Anyone with file access can edit the markdown files.

**Safeguards:**
- The UI clearly labels results as "retrieved patterns" rather than "AI answers"
- The reliability evaluator includes a test that verifies gibberish queries return no results, preventing false confidence

---

## Testing Results

The reliability evaluator runs 7 automated tests on every app load:

| Test | Result |
|------|--------|
| check_guess: correct guess returns Win | ✅ Pass |
| check_guess: high guess returns Too High | ✅ Pass |
| check_guess: low guess returns Too Low | ✅ Pass |
| parse_guess: valid input parses correctly | ✅ Pass |
| parse_guess: out-of-range input rejected | ✅ Pass |
| retriever: returns docs for known keyword | ✅ Pass |
| retriever: returns no docs for gibberish | ✅ Pass |

**7/7 tests passing.** The AI struggled when queries used synonyms not present in the knowledge base docs — for example "endless loop" failed to retrieve the infinite loop document. Accuracy improved after expanding keyword coverage in the docs.

---

## AI Collaboration Reflection

This project was built with significant AI assistance throughout the development process.

**Helpful suggestion:** When setting up the RAG retriever, the AI suggested using set intersection scoring as a simple and transparent alternative to embedding-based retrieval. This was genuinely useful — it kept the system dependency-free and easy to test, which turned out to matter a lot when external APIs kept failing during development.

**Flawed suggestion:** The AI repeatedly suggested using heredoc syntax (`<< 'EOF'`) to write file content from the terminal. In practice, this caused consistent failures because the terminal mangled multi-line pastes, especially with backticks and special characters inside the content. The actual fix was writing a Python script to create the files programmatically, which the AI only suggested after several failed attempts.

---

## Reflection: What This Project Says About Me as an AI Engineer

Building this project taught me that the hardest part of working with AI systems isn't the model — it's the infrastructure around it. I spent more time debugging API keys, deprecated models, and environment variables than I did on the actual RAG logic. That experience made me appreciate why reliability testing and guardrails matter so much. An AI feature that works 80% of the time and silently fails the other 20% is worse than a simpler system that works every time. The decision to remove the external API dependency and build a self-contained retrieval system was the right call — it made the app more reliable, more testable, and easier to explain.