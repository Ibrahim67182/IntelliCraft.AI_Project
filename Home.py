import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="Multi-Function App",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark mode + modern look
st.markdown("""
    <style>
        .stApp {
            background-color: #0b1f40;
            color: white;
        }
        .block-container {
            padding: 2rem;
        }
        h1, h2, h3 {
            color: #00d4ff;
        }
        .feature-card {
            background-color: #1a2d5a;
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            box-shadow: 0px 0px 15px rgba(0, 212, 255, 0.15);
        }
        a {
            color: #00d4ff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center;'>Welcome to the IntelliCraft</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Crafting Emails, Resumes, PDF Answers & Summaries with Intelligent Precision</p>", unsafe_allow_html=True)

# Intro or dashboard cards
st.markdown("## 🚀 Available Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>📧 <a href="/Email_Generator" target="_self">Email Generator</a></h3>
        <p>Generate professional, cold, or cover emails using AI assistance.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <h3>🧠 <a href="/ATS_Resume_Analyzer" target="_self">ATS Resume Analyzer</a></h3>
        <p>Upload your resume and get insights on how to optimize it for applicant tracking systems (ATS).</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>📄 <a href="/PDF_Chat" target="_self">PDF Chat</a></h3>
        <p>Upload any PDF and ask questions directly to extract relevant content.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <h3>📝 <a href="/Resume_Content_Generator" target="_self">Resume Content Generator</a></h3>
        <p>Let AI write optimized and relevant resume sections tailored to your field.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer or contact
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px; color: #cccccc;'>Developed By Ibrahim Junaid</p>", unsafe_allow_html=True)
