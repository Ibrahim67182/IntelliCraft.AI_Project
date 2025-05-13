

from langchain.prompts import PromptTemplate

import streamlit as st

from ctransformers import AutoModelForCausalLM

import pyperclip





# for running streamlit lib      : python -m stramlit run email_chatbot.py



# loading the model

@st.cache_resource  
def load_model():
        return AutoModelForCausalLM.from_pretrained(
        model_path_or_repo_id="D:/huggingface_models/model/mistral-7b-instruct-v0.1.Q4_K_M.gguf",           # replace this path with your own path 
            model_type="mistral",
            max_new_tokens= 512,      # limit output
                temperature = 0.85,         # balanced creativity
                top_k = 40,
                top_p = 0.95,
                repetition_penalty = 1.1
            
        
        )




# writing prompts for email templates to generate emails

cover_letter_template  = """"write a proper formal style cover letter to the {recipient} in a proper format having
 around three or four paragraphs and also include salutation, introduction, body, and closing for the context : {context} """



apology_template = """write a professional and humble apology mail in polite and respectable tone to {recipient} in order to resolve the 

misunderstanding about the issue described in the context. : {context}. Also provide proper format or structure used in it.
"""


request_template = """
you are efficient in bargaining now you need write impactful mail to convince {recipient} in order to
 fulfil your demands related to the subject : {context} . Also provide proper format or structure used in it.


"""

informal_template = """" You are a frank and friendly writer. Now write email to {recipient} 

using friendly tone like you are close to the person and have a good connection with the person about the context : {context}. 
Also provide proper format or structure used in it.


"""


resignation_template = """ the person wants to quit the job. Now you are humble respectful and polite writer who writes a letter to {recipient}

in order to in order to formally resign while expressing sincere gratitude. The reason and the context for writing this mail is : {context}. Also provide proper format or structure used in it.


"""


formal_template = """You are really a professional and highly qualified technical writer. Write the email to {recipient} in formal , respectful and highly professional

tone following the proper format using the rules of SCOPE. The subject to discuss in the mail is : {context}. Also provide proper format or structure used in it.


"""

cold_reach_template = """You are really smart and know how to outreach a stranger professionally. Your task is to persuade the {recipient} through

your solid reasoning and valid arguments on the subject: {context} in the form of cold outreach mail. Also provide proper format or structure used in it.
"""


invitation_template = """ 
You are really good host and know how to invite and honor in effective manner. Now write an invitation letter or mail to {recipient} 
whom you are inviting on the occasion: {context} 

in a really warmth and welcoming tone. Also provide proper format or structure used in it.


"""


thank_template = """Write a thanks email showing great respect and honor to {recipient} for helping out or assitance in : {context}. 
 Also provide proper format or structure used in it.

"""

follow_up_template = """ 
You are consistent, polite, and respectful. Now write a follow-up email to {recipient} regarding the subject: {context}. 

Maintain a tone that reflects curiosity without being pushy, and express genuine interest or need for an update. 
 Also provide proper format or structure used in it.
"""


job_inquiry_template = """ 
You are an enthusiastic and brilliant job seeker. Write a polite and professional email to {recipient} inquiring about any potential job openings or opportunities 

in the area of your interest, based on the context: {context}. Be humble, respectful, and show genuine interest in the organization.
 Also provide proper format or structure used in it.
"""



meeting_template = """ 
You are organized and professional. Now write an email to {recipient} in order to schedule or confirm a meeting regarding the topic: {context}.

Use a respectful and clear tone, include potential timings, and express appreciation for their time.
 Also provide proper format or structure used in it.
"""


complaint_template = """ 
You are a responsible and professional individual. Now write a formal and respectful complaint email to {recipient} about the issue related to: {context}.

Make sure to be factual, concise, and solution-oriented, while keeping the tone calm and constructive. Also provide proper format or structure used in it.
"""


farewell_template = """ 
Now you are leaving the workplace or team. Write a heartfelt farewell email to {recipient} expressing gratitude and memorable moments. 

The reason and the context for your departure is: {context}. Maintain a warm and respectful tone.
 Also provide proper format or structure used in it.
"""


introduction_template = """ 
You are meeting someone new in a professional setting. Write a polite and engaging introduction email to {recipient} to introduce yourself properly, 

highlighting key details from the context: {context}. Be clear, humble, and make a good first impression. Leave a great impact and 
impression on reader.
 Also provide proper format or structure used in it.
"""



job_rejection_template = """ 
You have received a job offer but decided not to accept it. Write a respectful and polite rejection email to {recipient} expressing your sincere gratitude for the opportunity.

The reason for rejection and context is: {context}. Keep the tone appreciative and professional. Use the rule of courtesy in this mail.

 Also provide proper format or structure used in it.
"""





email_templates = { 
    
    "cover_Letter": PromptTemplate.from_template(cover_letter_template),
   
    "Apology_Email": PromptTemplate.from_template(apology_template),
   
    "Request_Email": PromptTemplate.from_template(request_template),
   
    "Informal_Email": PromptTemplate.from_template(informal_template),
   
    "Resignation_Letter":PromptTemplate.from_template(resignation_template),
   
    "Formal_Email":PromptTemplate.from_template(formal_template),
    
    "Cold_Email":PromptTemplate.from_template(cold_reach_template),

    "Invitation_Letter":PromptTemplate.from_template(invitation_template),
    
    "Thank_You_Email": PromptTemplate.from_template(thank_template),

    "Follow_up_Email": PromptTemplate.from_template(follow_up_template) ,

    "Job_Inquiry_Email": PromptTemplate.from_template(job_inquiry_template),

    "Meeting_Email":  PromptTemplate.from_template(meeting_template), 
      
     "Complaint_Email": PromptTemplate.from_template(complaint_template) , 

     "Farewell_Email": PromptTemplate.from_template(farewell_template), 

     "Introduction_Email": PromptTemplate.from_template(introduction_template), 

     "Rejection_Email": PromptTemplate.from_template(job_rejection_template)



}




def email_generator_bot(email_type, recipient, context):
    input_prompt = email_templates.get(email_type) or email_templates["formal_email"]
   
    prompt = input_prompt.format(recipient=recipient, context=context)

    system_prompt = "You are a helpful assistant that writes high-quality emails."
    chat_prompt = f"""[INST] <<SYS>> {system_prompt} <</SYS>> {prompt} [/INST]"""

    # Generate the email using the model
    generated_email = llm_model(chat_prompt)

    return generated_email



llm_model = load_model()

email_types_list = [
  
    "cover_Letter",
    "Apology_Email",
    "Request_Email",
    "Informal_Email",
   
    "Resignation_Letter",
   
    "Formal_Email",
    "Cold_Email",

    "Invitation_Letter",
    
    "Thank_You_Email",

    "Follow_up_Email",
    "Job_Inquiry_Email",
    "Meeting_Email",
     "Complaint_Email",
     "Farewell_Email",
     "Introduction_Email",

     "Rejection_Email"

    
]



def main():

    

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





    # ------------------ Title ---------------------
    st.markdown("<h1 style='text-align: center; color: #00d4ff;'>✉️ AI Email Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cfcfcf;'>Generate polite, professional, and persuasive emails using LLaMA 2</p>", unsafe_allow_html=True)

   

    email_types = email_types_list

    email_type = st.selectbox("📧 Select Email Type", email_types)
    recipient = st.text_input("👤 Recipient Name", placeholder="e.g., Dr. Sarah Khan, Mr. Ahmed")
    context = st.text_area("📝 Context", placeholder="e.g., I need to reschedule our meeting due to travel.")

    if st.button("🚀 Generate Email"):
        if recipient and context:
            with st.spinner("Crafting your email..."):

                email = email_generator_bot(email_type, recipient, context)

                st.markdown("### ✅ Your AI-Generated Email")

            
                st.markdown(f"""
                        <div style='
                            background-color:#1a2b6d;
                            color:white;
                            padding:20px;
                            border-radius:12px;
                            margin-top:15px;
                            font-size:16px;
                            font-family: "Courier New", monospace;
                            min-height:300px;
                            max-height:600px;
                            overflow-y: auto;
                            white-space: pre-wrap;
                            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                        '>
                        <pre>{email}</pre>
                        </div>
                        """, unsafe_allow_html=True)


            # copy email button 
                if st.button("📋 Copy Email"):
                    pyperclip.copy(email)
                    st.success("Copied to clipboard!")
            
            # for email download
            
                st.download_button(
                    label="⬇️ Download Email",
                    data=email,
                    file_name="generated_email.txt",
                    mime="text/plain"
                            )
        

        else:
            st.warning("Please provide both recipient and context.")



