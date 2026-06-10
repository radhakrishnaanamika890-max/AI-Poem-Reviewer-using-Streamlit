import streamlit as st
import requests
import time

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Poem Reviewer",
    page_icon="📖",
    layout="wide"
)

# ---------------- CSS ---------------- #

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        -45deg,
        #ff0080,
        #ff4da6,
        #d633ff,
        #9933ff,
        #6600ff
    );
    background-size: 400% 400%;
    animation: luxury 10s ease infinite;
}

@keyframes luxury {
    0% {background-position:0% 50%;}
    50% {background-position:100% 50%;}
    100% {background-position:0% 50%;}
}

.main-box{
    background:rgba(255,255,255,0.12);
    backdrop-filter:blur(15px);
    padding:25px;
    border-radius:20px;
}

h1,h2,h3{
    color:white;
}

.stButton > button{
    background:linear-gradient(
        135deg,
        #ff4da6,
        #9333ea
    );
    color:white;
    border:none;
    border-radius:12px;
    width:100%;
    font-size:18px;
    font-weight:bold;
}

.review-box{
    background:white;
    color:black;
    padding:20px;
    border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #

st.sidebar.markdown("# 📖 AI Poem Reviewer")

st.sidebar.info(
    "Analyze poems using Ollama AI"
)

st.sidebar.write("### Available Features")
st.sidebar.write("✅ Theme Analysis")
st.sidebar.write("✅ Emotion Analysis")
st.sidebar.write("✅ Literary Devices")
st.sidebar.write("✅ Rating")
st.sidebar.write("✅ Download Review")

# ---------------- MAIN UI ---------------- #

st.markdown('<div class="main-box">', unsafe_allow_html=True)

st.title("📖 AI Poem Reviewer")

st.header("✨ Professional Poetry Analysis Platform")

st.markdown("""
Write your poem below and receive a professional AI review.
""")

# ---------------- SELECT BOX ---------------- #

poem_type = st.selectbox(
    "📚 Select Poem Type",
    [
        "General",
        "Love",
        "Nature",
        "Motivational",
        "Friendship",
        "Spiritual"
    ]
)

# ---------------- SLIDER ---------------- #

detail_level = st.slider(
    "🎚 Analysis Detail Level",
    1,
    10,
    5
)

# ---------------- FILE UPLOAD ---------------- #

uploaded_file = st.file_uploader(
    "📄 Upload Poem Text File",
    type=["txt"]
)

poem = ""

if uploaded_file:
    poem = uploaded_file.read().decode("utf-8")

# ---------------- TEXT AREA ---------------- #

poem = st.text_area(
    "✍️ Enter Your Poem",
    value=poem,
    height=250,
    placeholder="Type your poem here..."
)

# ---------------- METRICS ---------------- #

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📝 Words", len(poem.split()))

with col2:
    st.metric("🔤 Characters", len(poem))

with col3:
    st.metric("📄 Lines", len(poem.splitlines()))

# ---------------- INFO ---------------- #

st.write("Selected Type:", poem_type)
st.write("Detail Level:", detail_level)

# ---------------- BUTTON ---------------- #

if st.button("🚀 Analyze Poem"):

    if poem.strip():

        try:

            progress = st.progress(0)

            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)

            with st.spinner("🤖 AI is analyzing your poem..."):

                prompt = f"""
You are a professional poetry reviewer.

Poem Type: {poem_type}

Analysis Detail Level: {detail_level}/10

Analyze:

1. Theme
2. Emotion
3. Literary Devices
4. Strengths
5. Suggestions
6. Rating out of 10

Poem:

{poem}
"""

                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "llama3",
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=300
                )

                response.raise_for_status()

                result = response.json().get(
                    "response",
                    "No response generated."
                )

            st.success("✅ Analysis Completed")

            tab1, tab2 = st.tabs(
                ["🤖 AI Review", "📊 Statistics"]
            )

            with tab1:

                st.markdown(
                    f"""
<div class="review-box">
{result}
</div>
                    """,
                    unsafe_allow_html=True
                )

                st.download_button(
                    "📥 Download Review",
                    result,
                    file_name="poem_review.txt",
                    mime="text/plain"
                )

            with tab2:

                st.write("### Poem Statistics")

                st.write(
                    {
                        "Poem Type": poem_type,
                        "Words": len(poem.split()),
                        "Characters": len(poem),
                        "Lines": len(poem.splitlines()),
                        "Detail Level": detail_level
                    }
                )

            with st.expander("📖 Show Original Poem"):

                st.write(poem)

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Ollama server is not running."
            )

            st.info(
                "Run: ollama serve"
            )

        except requests.exceptions.Timeout:

            st.error(
                "❌ Ollama response timed out."
            )

        except Exception as e:

            st.error(
                f"❌ Error: {str(e)}"
            )

    else:

        st.warning(
            "⚠ Please enter a poem first."
        )

st.markdown("</div>", unsafe_allow_html=True)