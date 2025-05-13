import streamlit as st
from io import BytesIO
from langchain_community.llms import LlamaCpp  
from docx import Document
from pdfminer.high_level import extract_text_to_fp
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def main():


        # --------------------- Model Initialization ---------------------

        @st.cache_resource
        def load_model():
            return  LlamaCpp(
                model_path="D:/huggingface_models/model/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
                n_ctx=4096,
                max_tokens = 2048,
                temperature=0.8,
                top_p=0.95,
                verbose=True
            )


        llm = load_model()



        # --------------------- Resume Text Extractor ---------------------
        def extract_resume_text_from_bytes(file_bytes, file_ext):
            if file_ext == "pdf":
                output_string = BytesIO()
                extract_text_to_fp(BytesIO(file_bytes), output_string)
                return output_string.getvalue().decode()
            elif file_ext == "docx":
                doc = Document(BytesIO(file_bytes))
                return "\n".join([para.text for para in doc.paragraphs])
            else:
                raise ValueError("Unsupported file format. Please upload a PDF or DOCX.")


        # --------------------- Prompt Template ---------------------
        socre_prompt = PromptTemplate(
            input_variables=["resume_text"],
            template="""
        You are an ATS (Applicant Tracking System) simulator.

        Given the resume below:
        ---
        {resume_text}
        ---

        1. Give it an ATS score (out of 100).
        2. Mention specific suggestions to improve formatting, keywords, and structure for ATS systems.


        Output the result in clean, professional markdown format.
        """
        )



        improve_resume_prompt = PromptTemplate(
            input_variables=["resume_text"],
            template="""You are a professional Resume improver and improve resumes based on content given and make them ats friendly to stand out.

            Given the resume below:

            {resume_text}

        Your output should be a complete markdown-formatted resume with the following sections (if applicable):
        - **Name and Contact**
        - **Professional Summary**
        - **Skills**
        - **Work Experience**
        - **Projects**
        - **Education**
        - **Certifications**
        - **Languages**

        Use consistent formatting and make sure it's detailed enough for an ATS system to parse.

        Output only the improved resume in markdown format.


        """

        )



        # --------------------- Chain Setup ---------------------
        score_chain = LLMChain(llm=llm, prompt=socre_prompt)

        improvement_chain = LLMChain(llm=llm , prompt = improve_resume_prompt)



        # --------------------- Analysis Function ---------------------
        def analyze_resume(uploaded_file):
            file_bytes = uploaded_file.read()
            file_ext = uploaded_file.name.split('.')[-1].lower()
            resume_text = extract_resume_text_from_bytes(file_bytes, file_ext)

            if len(resume_text.strip()) == 0:
                return "❌ The resume file appears to be empty or unreadable."

            score_feedback = score_chain.run(resume_text=resume_text)
            improved_resume = improvement_chain.run(resume_text=resume_text)
            
            return score_feedback, improved_resume

        # --------------------- Streamlit UI ---------------------



        royal_blue_css = """
        <style>
            body {
                background-color: #0b1f40;
                color: #ffffff;
            }
            .stApp {
                background-color: #0b1f40;
            }
            .block-container {
                padding: 2rem;
                background-color: #0b1f40;
                border-radius: 10px;
            }
            .stTextInput input,
            .stTextArea textarea,
            .stSelectbox div[data-baseweb="select"] {
                background-color: #1a2d5a;
                color: #ffffff !important;
                border: 1px solid #3d5aa3;
                border-radius: 8px;
            }
            .stTextInput input::placeholder,
            .stTextArea textarea::placeholder {
                color: #b0b8d1;
            }
            .stButton>button {
                background-color: #1e3f9e;
                color: white;
                border-radius: 10px;
                height: 3em;
                font-size: 1rem;
                transition: all 0.3s ease;
                border: none;
            }
            .stButton>button:hover {
                background-color: #325bc7;
                transform: scale(1.03);
            }
        </style>
        """
        st.markdown(royal_blue_css, unsafe_allow_html=True)


        # Custom CSS
        st.markdown("""
            <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #f8f9fa; }
            .title { text-align: center; font-size: 36px; margin-bottom: 10px; }
            .subheader { text-align: center; font-size: 18px; color: gray; margin-bottom: 30px; }
            .report { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.05); }
            </style>
        """, unsafe_allow_html=True)

        # Title and Subheader


        st.markdown("<h1 style='text-align: center; color: #00d4ff;'>📝 Resume ATS Analyzer</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #cfcfcf;'>Upload your resume and receive feedback + ATS score</p>", unsafe_allow_html=True)


        uploaded = st.file_uploader("📎 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

        if uploaded:
            with st.spinner("🔍 Analyzing your resume, please wait..."):
                score_feedback, improved_resume = analyze_resume(uploaded)
            
            st.markdown('<div class="report">', unsafe_allow_html=True)
            st.markdown("### 📊 ATS Score & Suggestions")
            st.markdown(score_feedback)
            st.markdown("### ✨ Improved Resume (ATS-Optimized)")
            st.markdown(improved_resume)
            st.markdown('</div>', unsafe_allow_html=True)

