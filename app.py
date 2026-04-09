"""
app.py
~~~~~~
Game Glitch Investigator — extended with a RAG-powered bug pattern lookup
and a built-in reliability evaluation panel.
Tab 1: Original Glitchy Guesser number game.
Tab 2: Bug Pattern Lookup (RAG retrieval, no AI API required).
Tab 3: Reliability Evaluator (automated test harness).
"""

import os
import random
import logging
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score
from retriever import retrieve, format_context

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

st.set_page_config(page_title="Game Glitch Investigator", page_icon="🔍")
st.title("🔍 Game Glitch Investigator")

tab1, tab2, tab3 = st.tabs(["🎮 Glitchy Guesser", "📚 Bug Pattern Lookup", "🧪 Reliability Evaluator"])

# ── TAB 1: Original Game ──────────────────────────────────────────────────────
with tab1:
    st.caption("A number guessing game — now actually winnable.")

    st.sidebar.header("⚙️ Settings")
    difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Normal", "Hard"], index=1)
    attempt_limit_map = {"Easy": 10, "Normal": 7, "Hard": 5}
    attempt_limit = attempt_limit_map[difficulty]
    low, high = get_range_for_difficulty(difficulty)
    st.sidebar.caption(f"Range: {low} to {high}")
    st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

    if "current_difficulty" not in st.session_state:
        st.session_state.current_difficulty = difficulty
    if st.session_state.current_difficulty != difficulty:
        st.session_state.current_difficulty = difficulty
        st.session_state.secret = random.randint(low, high)
        st.session_state.attempts = 0
        st.session_state.score = 0
        st.session_state.status = "playing"
        st.session_state.history = []

    for k, v in [("secret", random.randint(low, high)), ("attempts", 0), ("score", 0),
                 ("status", "playing"), ("history", []), ("high_score", 0)]:
        if k not in st.session_state:
            st.session_state[k] = v

    def proximity_emoji(guess, secret, rng):
        ratio = abs(guess - secret) / rng
        if ratio <= 0.05: return "🔥 Scorching!"
        if ratio <= 0.15: return "♨️ Very warm"
        if ratio <= 0.30: return "😐 Lukewarm"
        if ratio <= 0.50: return "🧊 Cold"
        return "❄️ Freezing!"

    st.sidebar.divider()
    st.sidebar.subheader("🏆 High Score")
    st.sidebar.metric("Best score", st.session_state.high_score)

    with st.expander("🛠️ Developer Debug Info"):
        st.write("Secret:", st.session_state.secret)
        st.write("Attempts:", st.session_state.attempts)
        st.write("Score:", st.session_state.score)

    attempts_left = attempt_limit - st.session_state.attempts
    st.progress(attempts_left / attempt_limit, text=f"Attempts remaining: {attempts_left} / {attempt_limit}")
    st.info(f"Guess a number between **{low}** and **{high}**.")

    raw_guess = st.text_input("Enter your guess:", key=f"guess_input_{difficulty}")
    col1, col2, col3 = st.columns(3)
    with col1: submit = st.button("Submit Guess 🚀")
    with col2: new_game = st.button("New Game 🔁")
    with col3: show_hint = st.checkbox("Show hint", value=True)

    if new_game:
        st.session_state.attempts = 0
        st.session_state.secret = random.randint(low, high)
        st.session_state.status = "playing"
        st.session_state.score = 0
        st.session_state.history = []
        st.success("New game started!")
        st.rerun()

    if st.session_state.status != "playing":
        if st.session_state.status == "won":
            st.success("🎉 You already won! Start a new game to play again.")
        else:
            st.error("💀 Game over. Start a new game to try again.")
        st.stop()

    if submit:
        if not raw_guess or raw_guess.strip() == "":
            st.error("Enter a guess before submitting.")
        else:
            ok, guess_int, err = parse_guess(raw_guess, low, high)
            if not ok:
                st.session_state.history.append(raw_guess)
                st.error(err)
            else:
                st.session_state.attempts += 1
                st.session_state.history.append(guess_int)
                outcome, message = check_guess(guess_int, st.session_state.secret)
                if show_hint:
                    if outcome == "Win":
                        st.success(message)
                    elif outcome == "Too High":
                        st.error(f"📉 Go LOWER!  {proximity_emoji(guess_int, st.session_state.secret, high - low)}")
                    else:
                        st.warning(f"📈 Go HIGHER!  {proximity_emoji(guess_int, st.session_state.secret, high - low)}")
                st.session_state.score = update_score(
                    current_score=st.session_state.score,
                    outcome=outcome,
                    attempt_number=st.session_state.attempts,
                )
                if outcome == "Win":
                    st.balloons()
                    st.session_state.status = "won"
                    if st.session_state.score > st.session_state.high_score:
                        st.session_state.high_score = st.session_state.score
                        st.toast("🏆 New high score!", icon="🏆")
                    st.success(f"🎉 You won! The secret was **{st.session_state.secret}**. Final score: **{st.session_state.score}**")
                elif st.session_state.attempts >= attempt_limit:
                    st.session_state.status = "lost"
                    st.error(f"💀 Out of attempts! The secret was **{st.session_state.secret}**. Score: **{st.session_state.score}**")

    if st.session_state.history:
        st.divider()
        st.subheader("📋 Guess History")
        rows = []
        for i, g in enumerate(st.session_state.history, 1):
            if isinstance(g, int):
                direction = "✅ Correct!" if g == st.session_state.secret else ("📉 Too High" if g > st.session_state.secret else "📈 Too Low")
                prox = proximity_emoji(g, st.session_state.secret, high - low)
            else:
                direction, prox = "❌ Invalid", "—"
            rows.append({"#": i, "Guess": g, "Result": direction, "Proximity": prox})
        st.table(rows)

    st.divider()
    st.caption("Built by an AI that claims this code is production-ready.")

# ── TAB 2: Bug Pattern Lookup (RAG) ──────────────────────────────────────────
with tab2:
    st.markdown(
        "Describe a bug or paste code snippets below. "
        "The system retrieves relevant bug pattern docs from its knowledge base."
    )

    query = st.text_area(
        "Describe your bug or paste code:",
        height=150,
        placeholder="e.g. my while loop never stops running"
    )
    search_btn = st.button("Search Knowledge Base", type="primary")

    if search_btn:
        if not query.strip():
            st.warning("Please enter a description before searching.")
        else:
            docs = retrieve(query)
            logging.info(f"Retrieved {len(docs)} doc(s) for query: {query[:50]}")

            if not docs:
                st.warning("No matching patterns found. Try different keywords.")
            else:
                st.success(f"Found {len(docs)} relevant pattern(s):")
                for doc in docs:
                    with st.expander(f"📄 {doc['filename']}"):
                        st.markdown(doc["content"])

# ── TAB 3: Reliability Evaluator ─────────────────────────────────────────────
with tab3:
    st.markdown(
        "Run automated tests to verify the game logic and retriever are working correctly."
    )

    run_btn = st.button("Run All Tests", type="primary")

    if run_btn:
        results = []

        # test 1: check_guess correct
        try:
            outcome, _ = check_guess(42, 42)
            passed = outcome == "Win"
            results.append(("check_guess: correct guess returns Win", passed))
        except Exception as e:
            results.append((f"check_guess: correct guess returns Win", False))

        # test 2: check_guess too high
        try:
            outcome, _ = check_guess(80, 50)
            passed = outcome == "Too High"
            results.append(("check_guess: high guess returns Too High", passed))
        except Exception as e:
            results.append(("check_guess: high guess returns Too High", False))

        # test 3: check_guess too low
        try:
            outcome, _ = check_guess(20, 50)
            passed = outcome == "Too Low"
            results.append(("check_guess: low guess returns Too Low", passed))
        except Exception as e:
            results.append(("check_guess: low guess returns Too Low", False))

        # test 4: parse_guess valid input
        try:
            ok, val, _ = parse_guess("50", 1, 100)
            passed = ok and val == 50
            results.append(("parse_guess: valid input parses correctly", passed))
        except Exception as e:
            results.append(("parse_guess: valid input parses correctly", False))

        # test 5: parse_guess out of range
        try:
            ok, _, _ = parse_guess("999", 1, 100)
            passed = not ok
            results.append(("parse_guess: out-of-range input rejected", passed))
        except Exception as e:
            results.append(("parse_guess: out-of-range input rejected", False))

        # test 6: retriever returns results for known keyword
        try:
            docs = retrieve("infinite loop while")
            passed = len(docs) > 0
            results.append(("retriever: returns docs for known keyword", passed))
        except Exception as e:
            results.append(("retriever: returns docs for known keyword", False))

        # test 7: retriever returns empty for garbage input
        try:
            docs = retrieve("xyzzy foobar nonsense123")
            passed = len(docs) == 0
            results.append(("retriever: returns no docs for gibberish", passed))
        except Exception as e:
            results.append(("retriever: returns no docs for gibberish", False))

        # display results
        passed_count = sum(1 for _, p in results if p)
        st.markdown(f"### Results: {passed_count}/{len(results)} passed")
        for name, passed in results:
            if passed:
                st.success(f"✅ {name}")
            else:
                st.error(f"❌ {name}")

        logging.info(f"Reliability eval: {passed_count}/{len(results)} passed")