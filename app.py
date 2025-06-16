import streamlit as st
from transformers import pipeline
from pdfminer.high_level import extract_text
import uuid

# Set page config
st.set_page_config(page_title="📘 PDF Summarizer", page_icon="📄", layout="centered")

@st.cache_resource
def load_model():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_model()

# Extract PDF text
def extract_pdf_text(pdf_file):
    with open("temp.pdf", "wb") as f:
        f.write(pdf_file.read())
    return extract_text("temp.pdf")

# Split long text into chunks
def split_text(text, max_chunk=1000):
    paragraphs = text.split('\n')
    chunks, current_chunk = [], ""
    for para in paragraphs:
        if len(current_chunk) + len(para) <= max_chunk:
            current_chunk += para + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

# Summarize text
def summarize_text(text):
    chunks = split_text(text)
    summary_parts = []
    for chunk in chunks:
        result = summarizer(chunk, max_length=150, min_length=40, do_sample=False)[0]['summary_text']
        summary_parts.append(result)
    return "\n\n".join(summary_parts)

# Initialize session keys
if "file_key" not in st.session_state:
    st.session_state.file_key = str(uuid.uuid4())

# CSS styling
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 2.5em;
            font-family: Arial, sans-serif;
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 0.2em;
        }
        .subtitle {
            text-align: center;
            font-size: 1.2em;
            color: #777;
            margin-bottom: 2em;
            font-family: Arial, sans-serif;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white !important;
            font-weight: bold;
            font-family: Arial, sans-serif;
            border-radius: 8px;
            border: none;
            transition: background-color 0.3s ease, box-shadow 0.2s ease;
        }
        .stButton > button:hover {
            background-color: #388E3C;
            box-shadow: 0 0 0 3px rgba(56, 142, 60, 0.4);
            cursor: pointer;
        }
        .stDownloadButton button {
            background-color: #4CAF50;
            color: white !important;
            font-weight: bold;
            font-family: Arial, sans-serif;
            border-radius: 8px;
            border: none;
            transition: background-color 0.3s ease, box-shadow 0.2s ease;
            padding: 0.6rem 1.5rem;
            font-size: 16px;
        }
        .stDownloadButton button:hover {
            background-color: #388E3C;
            box-shadow: 0 0 0 3px rgba(56, 142, 60, 0.4);
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# Title + Instructions
st.markdown('<div class="title">📄 AI-Powered PDF Summarizer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload a PDF document and get a smart summary...</div>', unsafe_allow_html=True)

# Upload with dynamic key
uploaded_pdf = st.file_uploader("📤 Upload PDF File", type=["pdf"], key=st.session_state.file_key)

# Summarize
if uploaded_pdf is not None and "summary" not in st.session_state:
    with st.spinner("⏳ Extracting text from PDF..."):
        text = extract_pdf_text(uploaded_pdf)

    if text:
        st.success("✅ Text extracted successfully!")

        if st.button("🧠 Summarize Now"):
            with st.spinner("✍️ Generating summary..."):
                st.session_state.summary = summarize_text(text)
    else:
        st.error("❌ Failed to extract text from PDF.")

# Summary display
if "summary" in st.session_state:
    st.subheader("📜 Summary")
    st.write(st.session_state.summary)
    st.markdown("---")

    summary_filename = f"summary_{uuid.uuid4().hex[:8]}.txt"
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📥 Download Summary",
            data=st.session_state.summary,
            file_name=summary_filename,
            mime="text/plain",
            use_container_width=True,
            key="download_summary"
        )

    st.markdown("### ✅ Summary ready!")
    if st.button("🔄 Summarize Another PDF"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.file_key = str(uuid.uuid4())  # Refresh uploader
        st.rerun()

# Footer
st.markdown("""
---
<center style="color:#999">AI-Powered PDF Summarizer</center>
""", unsafe_allow_html=True)
