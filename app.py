import streamlit as st
import os
import requests

# ------------------------- Page Config -------------------------
st.set_page_config(page_title="YouTube Script Writer", layout="wide")

# ------------------------- CSS Styling -------------------------
st.markdown("""
<style>
body { font-family: 'Segoe UI', sans-serif; }
.big-title { font-size: 36px; font-weight: 700; margin-bottom: 5px; }
.sub { color: #555; margin-bottom: 20px; }
.card { padding: 20px; background: #f8f9fa; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# ------------------------- Header -------------------------
st.markdown("<div class='big-title'>🎬 YouTube Script Writer</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Generate full YouTube video scripts instantly using AI.</div>", unsafe_allow_html=True)
st.markdown("---")

# ------------------------- OpenRouter Client -------------------------
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "x-ai/grok-4.1-fast:free"

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

# ------------------------- Tool Inputs -------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
topic = st.text_input("Video Topic / Idea:", "How AI is changing productivity")
style = st.selectbox("Video Style:", ["Informative", "Tutorial", "Storytelling", "Funny/Entertainment"])
length = st.slider("Approx Script Length (words):", 200, 2000, 800)

if st.button("Generate Script"):
    prompt = f"Write a full YouTube video script on the topic: '{topic}'. Style: {style}. Approx length: {length} words. Include intro, main content, and outro, suitable for YouTube."
    with st.spinner("⏳ Generating script..."):
        output = generate_script(prompt)
    st.text_area("Generated Script", value=output, height=500)

st.markdown("</div>", unsafe_allow_html=True)
