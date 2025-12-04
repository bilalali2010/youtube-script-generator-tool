import streamlit as st
import os
import requests

# ------------------------- Page Config -------------------------
st.set_page_config(
    page_title="YouTube Script Writer",
    page_icon="🎬",
    layout="wide",
)

# ------------------------- CSS Styling -------------------------
st.markdown("""
<style>
body { font-family: 'Segoe UI', sans-serif; background-color: #f4f6f8; }
h1 { font-weight: 700; color: #0f6fff; }
.card { background: #ffffff; border-radius: 16px; padding: 25px; box-shadow: 0 8px 25px rgba(0,0,0,0.08); margin-bottom: 20px; }
.label { font-weight: 600; margin-bottom: 5px; color: #333; }
small { color: #555; }
button[kind="primary"] { border-radius: 10px !important; }
textarea { font-family: 'Segoe UI', sans-serif; }
</style>
""", unsafe_allow_html=True)

# ------------------------- Header -------------------------
st.markdown("<h1>🎬 YouTube Script Writer</h1>", unsafe_allow_html=True)
st.markdown("<small>Generate professional, ready-to-record YouTube video scripts instantly.</small>", unsafe_allow_html=True)
st.markdown("---")

# ------------------------- OpenRouter Client -------------------------
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "arcee-ai/trinity-mini:free"

def generate_script(prompt: str):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "❌ Error: OPENROUTER_API_KEY not set in environment or Streamlit secrets."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        resp = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ API Request Error: {str(e)}"

# ------------------------- Layout -------------------------
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='label'>Video Topic / Idea</div>", unsafe_allow_html=True)
    topic = st.text_input("", "How AI is changing productivity")

    st.markdown("<div class='label'>Video Style</div>", unsafe_allow_html=True)
    style = st.selectbox("", ["Informative", "Tutorial", "Storytelling", "Funny/Entertainment"])

    st.markdown("<div class='label'>Approx Script Length (words)</div>", unsafe_allow_html=True)
    length = st.slider("", 200, 2000, 800)

    st.markdown("<div class='label'>Optional Notes</div>", unsafe_allow_html=True)
    notes = st.text_area("", "", height=80, placeholder="Add special instructions or tone here (optional)")

    generate_btn = st.button("Generate Script", key="generate")

    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='label'>Generated YouTube Script</div>", unsafe_allow_html=True)

    if generate_btn:
        prompt = f"Write a professional YouTube script on the topic: '{topic}'. Style: {style}. Approx {length} words. {notes}"
        with st.spinner("⏳ Generating script..."):
            output = generate_script(prompt)
        st.text_area("", value=output, height=500, key="output_text")

        c1, c2 = st.columns(2)
        with c1:
            st.button("Copy to Clipboard", on_click=lambda: st.experimental_set_query_params(script_text=output))
        with c2:
            st.download_button("Download .txt", output, file_name=f"{topic.replace(' ','_')}_script.txt", mime="text/plain")
    else:
        st.info("Your generated script will appear here once you click 'Generate Script'.", icon="ℹ️")

    st.markdown("</div>", unsafe_allow_html=True)
