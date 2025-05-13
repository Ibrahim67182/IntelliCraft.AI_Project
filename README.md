# 🤖 IntelliCRaft – AI-Powered Productivity Assistant

**IntelliCRaft** is an AI-powered assistant built using the **Mistral-7B-Instruct** model. It helps you create emails, build resume content, evaluate your resume's ATS score, and even summarize or interact with PDFs using natural language.

---

## 🚀 Features

- ✅ **Email Generator**  
  Create formal, personalized, or job-related emails from simple input prompts.

- ✅ **Resume Content Generator**  
  Generate entire resumes based on user-provided data.

- ✅ **Resume ATS Analyzer**  
  Upload your PDF or DOCX resume to:
  - Score it for ATS-friendliness.
  - Get improvement suggestions.
  - Generate an optimized plain-text version.

- ✅ **PDF Tools**
  - 📄 Summarize uploaded PDFs.
  - ❓ Ask natural language questions about the content.

---


## 📺 YouTube Demo

[![IntelliCRaft Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID_HERE/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID_HERE)




## 🛠️ Setup Instructions

### 1. Download the Model

This app uses the following model from Hugging Face:

**🔗 Model:** `mistral-7b-instruct-v0.1.Q4_K_M.gguf`  
**📥 Download here:** [HuggingFace Link](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/tree/main)

> After downloading, note the full file path where the `.gguf` model is saved.


### 2. Update the Model Path

In the Python files, find the line that looks like:

python
model_path = "D:/huggingface_models/model/mistral-7b-instruct-v0.1.Q4_K_M.gguf"

And replace them with your actual path where you downloaded or saved the model.


### 3. Install Required Packages
Make sure you have Python installed. Then, install the required packages:


### 4. Run the App
Run the app locally using the following command:

python -m streamlit run Home.py

This will launch the app in your default web browser at LocalHost.


### 📂 Suggested Folder Structure



📁 IntelliCRaft/
├── Home.py

├── pdf_chat.py

├── resume_analyzer.py

├── resume_content.py

├── email_chatbot.py

├── pages/

│   ├── ATS_Resume_Analyzer.py

│   ├── Email_Generator.py

│   ├── PDF_Chat.py

│   └── Resume_Content_Gnerator.py


### 💡 Example Use Cases

🔹 Compose a professional job inquiry email.

🔹 Summarize lengthy reports, research papers, or contracts.

🔹 Get ATS-friendly resume feedback and suggestions.

🔹 Ask questions like:
"What is the conclusion of this PDF?"
"List all key dates in this document."


### 🧰 Built With

1- Streamlit Python 

2- LangChain

3- Mistral 7B Instruct (GGUF)


### 🙌 Credits
Developed by Ibrahim Junaid




