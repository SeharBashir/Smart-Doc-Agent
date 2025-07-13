

import streamlit as st
from agents import run_summarizer, run_insight_agent
import textract
import os
import tempfile

# Configure page
st.set_page_config(
    page_title="Smart Document Agents",
    layout="wide",
    page_icon="📄"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .stTextArea textarea {
            min-height: 250px;
        }
        .stButton>button {
            background-color: #7f1d1d;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 0.25rem;
            font-weight: 500;
        }
        .stButton>button:hover {
            background-color: #9f2d2d;
            color: white;
        }
        .header {
            color: #7f1d1d;
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
        }
        .success-box {
            background-color: #f0fff4;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #38a169;
            margin-bottom: 1rem;
        }
        .error-box {
            background-color: #fff5f5;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #e53e3e;
            margin-bottom: 1rem;
        }
        .entity-card {
            background-color: white;
            border-radius: 0.5rem;
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='header'>📄 Smart Document Agents</h1>", unsafe_allow_html=True)
st.markdown("Upload a document to extract summaries, entities, and sentiment analysis.")

# File uploader
uploaded_file = st.file_uploader(
    "📤 Upload a document (TXT, PDF, DOCX, DOC)",
    type=["txt", "pdf", "docx", "doc"],
    help="Supported formats: .txt, .pdf, .docx, .doc"
)

if uploaded_file is not None:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name

        # Use textract with explicit encoding handling
        try:
            text = textract.process(temp_path).decode("utf-8", errors="replace")
        except UnicodeDecodeError:
            # Fallback to latin-1 if utf-8 fails
            text = textract.process(temp_path).decode("latin-1", errors="replace")

        if not text.strip():
            st.warning("⚠️ The document appears to be empty or couldn't be extracted properly.")
        else:
            with st.expander("📃 View Original Text", expanded=False):
                st.text_area("Full Text", text, height=300, label_visibility="collapsed")

            run = st.button("🚀 Analyze Document", use_container_width=True)

            if run:
                # Create columns for results
                col1, col2 = st.columns(2)

                with col1:
                    with st.spinner("🔍 Extracting summary..."):
                        summary = run_summarizer(text)
                    st.markdown("### 🧾 Summary")
                    st.markdown('<div class="success-box">✅ Summary generated successfully</div>', unsafe_allow_html=True)
                    st.markdown(summary)

                with col2:
                    with st.spinner("🔎 Analyzing content..."):
                        entities, sentiment = run_insight_agent(text)
                    st.markdown("### 🔍 Named Entities")
                    st.markdown('<div class="success-box">✅ Entity extraction completed</div>', unsafe_allow_html=True)
                    
                    for ent in entities:
                        st.markdown(f"""
                            <div class="entity-card">
                                <strong>{ent[0]}</strong><br>
                                <small>Type: <em>{ent[1]}</em></small>
                            </div>
                        """, unsafe_allow_html=True)

                    st.markdown("### 😊 Sentiment Analysis")
                    st.markdown('<div class="success-box">✅ Sentiment analyzed</div>', unsafe_allow_html=True)
                    
                    # Visual sentiment indicators
                    polarity_emoji = "😊" if sentiment.polarity > 0.1 else "😐" if sentiment.polarity > -0.1 else "😞"
                    subjectivity_emoji = "🧠" if sentiment.subjectivity > 0.5 else "📊"
                    
                    st.markdown(f"""
                        <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
                            <div style="flex: 1; background: white; padding: 1rem; border-radius: 0.5rem; text-align: center;">
                                <div style="font-size: 2rem;">{polarity_emoji}</div>
                                <div>Polarity: <code>{sentiment.polarity:.2f}</code></div>
                                <small>{'Positive' if sentiment.polarity > 0.1 else 'Neutral' if sentiment.polarity > -0.1 else 'Negative'}</small>
                            </div>
                            <div style="flex: 1; background: white; padding: 1rem; border-radius: 0.5rem; text-align: center;">
                                <div style="font-size: 2rem;">{subjectivity_emoji}</div>
                                <div>Subjectivity: <code>{sentiment.subjectivity:.2f}</code></div>
                                <small>{'Subjective' if sentiment.subjectivity > 0.5 else 'Objective'}</small>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

        # Clean up
        os.remove(temp_path)

    except Exception as e:
        st.markdown(f"""
            <div class="error-box">
                ❌ Error processing file: {str(e)}
            </div>
        """, unsafe_allow_html=True)
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)