import streamlit as st
from streamlit_option_menu import option_menu
from langchain_community.llms import LlamaCpp
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from io import BytesIO
from docx import Document
from pdfminer.high_level import extract_text_to_fp
import base64
import streamlit.components.v1 as components



def main():



        # Custom UI CSS
        st.markdown("""
        <style>
            body, .stApp {
                background-color: #0b1f40;
                color: white;
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
            .chat-container {
                background-color: #2a2d40;
                border-radius: 12px;
                padding: 15px;
                margin-bottom: 10px;
                position: relative;
            }
            .chat-message {
                padding-right: 60px;
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("<h1 style='text-align: center; color: #00d4ff;'>📄 PDF Extractor Tool</h1>", unsafe_allow_html=True)
        st.markdown("---")

        @st.cache_resource
        def load_model():
            return LlamaCpp(
                model_path="D:/huggingface_models/model/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
                n_ctx=4096,
                max_tokens=2048,
                temperature=0.8,
                top_p=0.95,
                verbose=True
            )

        llm = load_model()




        selected = option_menu(
            menu_title=None,
            options=["Upload File", "PDF Summarizer", "PDF Q&A"],
            icons=["cloud-upload", "file-earmark-text", "chat-left-text"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#2c2f3a"},
                "icon": {"color": "#61dafb", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "center",
                    "margin": "5px",
                    "color": "#cfd3ec",
                    "--hover-color": "#3c3f4a",
                },
                "nav-link-selected": {"background-color": "#007BFF", "color": "white"},
            }
        )

        def extract_text(file_bytes, file_ext):
            if file_ext == "pdf":
                output_string = BytesIO()
                extract_text_to_fp(BytesIO(file_bytes), output_string)
                return output_string.getvalue().decode()
            elif file_ext == "docx":
                doc = Document(BytesIO(file_bytes))
                return "\n".join([para.text for para in doc.paragraphs])
            else:
                raise ValueError("Unsupported file format. Please upload a PDF or DOCX.")

        summary_words = ["100-300", "500-800", "1000-1500", "1500-2000"]

        summarizer_prompt = PromptTemplate(
            input_variables=['summary_content', 'summary_length'],
            template="""
        You are a professional content summarizer. Read the following content and generate a summary with an approximate word count of {summary_length}.
        Only provide summary on the content provided and nothing else.

        Content:
        {summary_content}

        Summary:
        """
        )

        q_ans_prompt = PromptTemplate(
            input_variables=['q_ans_content', 'question_asked'],
            template="""
        You are an intelligent assistant. Answer the question based only on the content below.

        Content:
        {q_ans_content}

        Question:
        {question_asked}

        Answer:
        """
        )

        def chunk_text(text, chunk_size=1000, overlap=200):
            words = text.split()
            chunks = []
            start = 0
            while start < len(words):
                end = min(start + chunk_size, len(words))
                chunks.append(" ".join(words[start:end]))
                start += chunk_size - overlap
            return chunks

        def summary_creator(content, summary_size):
            summary_chain = LLMChain(llm=llm, prompt=summarizer_prompt)
            return summary_chain.invoke({"summary_content": content, "summary_length": summary_size})

        def long_summary_creator(text, summary_size):
            chunks = chunk_text(text)
            summarized_chunks = [summary_creator(chunk, summary_size)["text"] for chunk in chunks]
            return "\n\n".join(summarized_chunks)

        def Q_ans_solver(content, question):
            q_ans_chain = LLMChain(llm=llm, prompt=q_ans_prompt)
            chunks = chunk_text(content)
            for chunk in chunks:
                try:
                    answer = q_ans_chain.invoke({"q_ans_content": chunk, "question_asked": question})
                    if answer and len(answer["text"].strip()) > 10:
                        return answer["text"]
                except:
                    continue
            return "Sorry, I couldn't find the answer in the document."

        def semantic_qa(question, full_text):
            chunks = chunk_text(full_text)
            scored = [(len(set(question.lower().split()) & set(chunk.lower().split())), chunk) for chunk in chunks]
            scored.sort(reverse=True)
            top_chunks = [text for score, text in scored[:3] if score > 0]
            return Q_ans_solver("\n\n".join(top_chunks), question)





        # Session State Initialization
        if "file" not in st.session_state:
            st.session_state.file = None
            st.session_state.file_bytes = None
            st.session_state.file_ext = None
            st.session_state.extracted_text = ""

        # File Upload
        if selected == "Upload File":
            uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])
            if uploaded_file:
                st.session_state.file = uploaded_file
                st.session_state.file_bytes = uploaded_file.read()
                st.session_state.file_ext = uploaded_file.name.split('.')[-1].lower()
                st.session_state.extracted_text = extract_text(st.session_state.file_bytes, st.session_state.file_ext)
                st.success(f"Uploaded: {uploaded_file.name}")

        # Summary Tab
        elif selected == "PDF Summarizer":
            if st.session_state.file:
                st.markdown("## 🧠 Summary Generator")
                st.write(f"**File:** `{st.session_state.file.name}`")
                summary_length = st.selectbox("Choose summary length (word count):", summary_words)

                if st.button("📝 Generate Summary"):
                    with st.spinner("Generating summary... Please wait."):
                        result = long_summary_creator(st.session_state.extracted_text, summary_length)
                    st.markdown("### 📄 Summary Output")
                    st.markdown(f"""
                        <div style='background-color: #2a2d40; padding: 20px; border-radius: 10px; color: white;'>{result}</div>
                    """, unsafe_allow_html=True)

                    # Download button
                    b64 = base64.b64encode(result.encode()).decode()
                    href = f'<a href="data:file/txt;base64,{b64}" download="summary.txt" style="color:#61dafb;">📥 Download Summary</a>'
                    st.markdown(href, unsafe_allow_html=True)
            else:
                st.warning("Please upload a file first from the **Upload File** tab.")

        # Q&A Tab
        elif selected == "PDF Q&A":
            if st.session_state.file:
                st.markdown("## 💬 Chat with your PDF/DOC")
                st.write(f"**File:** `{st.session_state.file.name}`")

                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []

                question = st.text_input("Ask something about the content...")

                if st.button("🔍 Get Answer") and question.strip():
                    with st.spinner("Searching for the answer..."):
                        answer = semantic_qa(question, st.session_state.extracted_text)
                    st.session_state.chat_history.append({"user": question, "bot": answer})

                if st.session_state.chat_history:
                    st.markdown("### 🤖 Chat History")
                    for idx, chat in enumerate(reversed(st.session_state.chat_history)):
                        st.markdown(f"""
                            <div class='chat-container'>
                                <div class='chat-message'>
                                    <b style='color:#61dafb;'>You:</b><br>{chat['user']}<br>
                                    <b style='color:#00ffcc;'>AI:</b><br>{chat['bot']}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("Please upload a file first from the **Upload File** tab.")


