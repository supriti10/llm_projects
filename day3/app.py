import streamlit as st
import time
import concurrent.futures

from players.gemini_flash import get_gemini_flash_response
from players.gemini_pro import get_gemini_pro_response
from players.groq import get_groq_response
from players.ollama_phi3 import get_phi3_response

from utils.prompts import get_prompt
from utils.scoring import score_responses

st.set_page_config(page_title="LLM Battle Arena", layout="wide")

st.title("🔥 LLM Battle Arena")

mode = st.selectbox("Game Mode", ["Normal", "Creative", "Logic", "Debate"])
user_input = st.text_area("Enter Prompt")

debug_box = st.empty()

def run_model(player, prompt):
    name, func = player
    start = time.time()

    try:
        print(f"🚀 {name} CALLED")
        result = func(prompt)
        print(f"✅ {name} FINISHED")
    except Exception as e:
        result = f"❌ Failed: {str(e)}"
        print(f"❌ {name} CRASHED:", e)

    end = time.time()
    return (name, result, round(end - start, 2))


if st.button("🚀 Start Battle"):

    if not user_input.strip():
        st.warning("Enter a prompt!")
        st.stop()

    prompt = get_prompt(mode, user_input)

    players = [
        ("Gemini Flash ⚡", get_gemini_flash_response),
        ("Gemini Pro 🧠", get_gemini_pro_response),
        ("Groq ⚡", get_groq_response),
        ("Phi3 🤖", get_phi3_response),
    ]

    st.info("⚡ Running models in parallel...")

    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(run_model, p, prompt) for p in players]

        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            results.append(res)

            debug_box.write(f"✔️ Completed: {res[0]} ({res[2]}s)")

    st.subheader("🧠 Responses")

    cols = st.columns(4)

    for i, (name, text, t) in enumerate(results):
        with cols[i]:
            st.markdown(f"### {name}")
            st.caption(f"⏱️ {t} sec")
            st.write(text)

    st.subheader("🏆 Vote Winner")
    vote = st.radio("Choose best:", [r[0] for r in results])

    if st.button("Submit Vote"):
        st.success(f"You voted for {vote}")

    st.subheader("📊 Scores")
    scores = score_responses([r[1] for r in results])
    st.json(scores)