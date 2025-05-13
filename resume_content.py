
from langchain.prompts import PromptTemplate
from ctransformers import AutoModelForCausalLM

from langchain.chains import LLMChain , SequentialChain
from langchain_community.llms  import LlamaCpp 
import re
import streamlit as st







@st.cache_resource
def load_resume_model():
        return LlamaCpp (

        model_path="D:/huggingface_models/model/mistral-7b-instruct-v0.1.Q4_K_M.gguf",           # replace this path with your own path 
        n_ctx=4096,
        max_tokens = 1500,
        temperature=0.8,
        top_p=0.95,
        verbose=True
               
        )




resume_bot_model = load_resume_model()


#-------------------------------------------------------------------------------------------------------

def generate_resume_fields(resume_data, llm):
    chains = []

    def make_chain(prompt_template_str, input_variables, output_key):
        prompt = PromptTemplate(template=prompt_template_str, input_variables=input_variables)
        return LLMChain(llm=llm, prompt=prompt, output_key=output_key)

    # Objective Chain
    objective_template = "Write a professional and precise career objective of 3-4 lines max for a resume for {name} based in {city}, {state}."
    chains.append(make_chain(objective_template, ['name', 'city', 'state'], 'generated_objective'))

    # Summary Chain
    summary_template = "Write a precise 5-6 lines professional summary for the context provided: {summary}."
    chains.append(make_chain(summary_template, ['summary'], 'generated_summary'))

    # Skills Chain
    skills_template = "List key technical skills and soft skills  for someone experienced in {skills}. Properly list down skills using bullet points with proper headings."
    chains.append(make_chain(skills_template, ['skills'], 'generated_skills'))

    # Education Chain (handle first entry only)
    edu = resume_data.get('education', [{}])[0]
    if edu:
        education_template = "Write an education section for {degree} from {university} graduated in {graduation_year}. Properly display these attributes of education with headings. Only display provided education."
        chains.append(make_chain(education_template, ['degree', 'university', 'graduation_year'], 'generated_education'))

    # Experience Chain (handle first entry only)
    exp = resume_data.get('experience', [{}])[0]
    if exp:
        experience_template = "Write a breifly and precisely work experience section for {title} at {company} ({duration}) with responsibilities: {details}. Use bullet points format to highlight experiences."
        chains.append(make_chain(experience_template, ['title', 'company', 'duration', 'details'], 'generated_experience'))

    # Projects Chain
    proj_titles = ', '.join([proj['title'] for proj in resume_data.get('projects', [])])
    if proj_titles:
        projects_template = "Write a projects section for projects: {project_titles}. Use bullet points to describe what is achieved in project with proper headings. Only display relevant achievements "
        chains.append(make_chain(projects_template, ['project_titles'], 'generated_projects'))

    # Certifications Chain
    cert_titles = ', '.join(resume_data.get('certifications', []))
    if cert_titles:
        certifications_template = "List certifications: {certifications}. List down certifications in pointer style with main heading only. Also write one line description of each certificate."
        chains.append(make_chain(certifications_template, ['certifications'], 'generated_certifications'))

    # Combine all chains
    overall_chain = SequentialChain(
        chains=chains,
        input_variables=['name', 'city', 'state', 'summary', 'skills', 'degree', 'university', 'graduation_year',
                         'title', 'company', 'duration', 'details', 'project_titles', 'certifications'],
        output_variables=['generated_objective', 'generated_summary', 'generated_skills', 'generated_education', 'generated_experience', 'generated_projects', 'generated_certifications'],
        verbose=True
    )

    # Prepare input data for the chain
    chain_input = {
        'name': resume_data.get('name', ''),
        'city': resume_data.get('city', ''),
        'state': resume_data.get('state', ''),
        'summary': resume_data.get('summary', ''),
        'skills': ', '.join(resume_data.get('skills', [])),
        'degree': edu.get('degree', ''),
        'university': edu.get('university', ''),
        'graduation_year': edu.get('graduation_year', ''),
        'title': exp.get('title', ''),
        'company': exp.get('company', ''),
        'duration': exp.get('duration', ''),
        'details': ', '.join(exp.get('details', [])),
        'project_titles': proj_titles,
        'certifications': cert_titles
    }

    # Run the chain and get results
    result = overall_chain.invoke(chain_input)
    
    generated_resume = {
    'objective': result.get('generated_objective', ''),
    'summary': result.get('generated_summary', ''),
    'skills': result.get('generated_skills', ''),
    'education': result.get('generated_education', ''),
    'experience': result.get('generated_experience', ''),
    'projects': result.get('generated_projects', ''),
    'certifications': result.get('generated_certifications', ''),
}


    return generated_resume



#---------------------------------------------------------------------------------------------

def display_generated_resume(resume_data, generated_sections):
    st.title("Generated Resume")

    st.markdown(f"**Name:** {resume_data['name']}")
    st.markdown(f"**Email:** {resume_data['email']}")
    st.markdown(f"**Phone:** {resume_data['phone']}")
    st.markdown(f"**Location:** {resume_data['city']}, {resume_data['state']}")
    st.markdown(f"**LinkedIn:** {resume_data['linkedin']}")
    st.markdown(f"**GitHub:** {resume_data['github']}")

    st.markdown("---")
    st.header("Objective")
    st.write(generated_sections['objective'])

    st.header("Professional Summary")
    st.write(generated_sections['summary'])

    st.header("Skills")
    st.write(generated_sections['skills'])

    st.header("Education")
    st.write(generated_sections['education'])

    st.header("Experience")
    st.write(generated_sections['experience'])

    st.header("Projects")
    st.write(generated_sections['projects'])

    st.header("Certifications")
    st.write(generated_sections['certifications'])

    st.markdown("---")

               

#------------------------------------------------------------------------------------------


def generate_resume_pdf():

        
     # taking user input of resume template from given option 


# Set page config for better layout and appearance
        # st.set_page_config(page_title="Resume Builder", page_icon="📄", layout="centered")

      

    
        # Add custom CSS for modern visuals
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


        # Title and Template Selection

        st.markdown("<h1 style='text-align: center; color: #00d4ff;'>✉️ Modern Resume Generator</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #cfcfcf;'>Generate professional and optimized content for your resume using LLaMA 2</p>", unsafe_allow_html=True)


        
       

       

        # Basic Information Section
        st.subheader("Basic Information")

        # Input fields with placeholder text to guide the user
        name = st.text_input("Name", placeholder="John Doe")
        city = st.text_input("City", placeholder="Karachi")
        state = st.text_input("State" , placeholder="Sindh")
        email = st.text_input("Email", placeholder="john.doe@example.com")
        phone = st.text_input("Phone Number", placeholder="03xx-xxxxxxx")  # Pakistan phone format
        linkedin = st.text_input("LinkedIn Account", placeholder="https://www.linkedin.com/in/johndoe/")
        github = st.text_input("Github Account", placeholder="http://github.com/Ibrahim67182")

        # Validate phone number input (Pakistan phone number format)
        def validate_phone_number(phone_number):
            pattern = r"^03\d{2}-\d{7}$"  # Pattern for phone numbers starting with 03xx-xxxxxxx
            if not re.match(pattern, phone_number):
                st.error("Please enter a valid Pakistan phone number (e.g., 03xx-xxxxxxx).")
                return False
            return True

        # Check if the phone number format is correct
        if phone and not validate_phone_number(phone):
            phone = ""

        # Objective Section
        st.subheader("Objective")
        objective = st.text_input("Objective", placeholder="State your career goal and value.")

        # Summary Section
        st.subheader("Summary")
        summary = st.text_area("Summary", placeholder="Summarize your skills and experience.")

        # Education Section
        st.subheader("Education")
        degree = st.text_input("Degree", placeholder="Bachelor of Science in Computer Science")
        uni = st.text_input("University", placeholder="University Name")

        # Dropdown for selecting the graduation year
        years = [str(year) for year in range(1950, 2051)]  # List of years from 2000 to 2025
        grad_year = st.selectbox("Graduation Year", years)

        
        # adding skills using skills session state

        st.subheader("Skills")
        
        if "skills" not in st.session_state:
            st.session_state.skills = []


        skill_input = st.text_input("Add a skill")
        
        if st.button("Add Skill"):
            if skill_input:
                 if skill_input not in [s.lower() for s in st.session_state.skills]:
                    
                    st.session_state.skills.append(skill_input)
                    
                    st.success(f"'{skill_input}' added to skills!")
                 else:
                    st.warning(f"'{skill_input}' is already in the skills list.")
        else:
             st.warning("Please enter a skill.")
          

          # projects adding session

        st.subheader("Projects")

        if "projects" not in st.session_state:
            st.session_state.projects = []

        # Show form when button clicked
        if st.button("Add Project"):
            st.session_state.show_project_form = True
        else:
            st.session_state.show_project_form = st.session_state.get("show_project_form", False)


        if st.session_state.show_project_form:
            with st.form(key="project_form"):
                project_title = st.text_input("Project Title", placeholder="e.g. AI Resume Builder")
                project_description = st.text_area("Project Description", placeholder="Short summary of the project")
                submitted = st.form_submit_button("Save Project")

                if submitted:
                    if project_title.strip() and project_description.strip():
                        # Check for duplicates by title and description
                        is_duplicate = any(
                            proj["title"].strip().lower() == project_title.strip().lower() and
                            proj["description"].strip().lower() == project_description.strip().lower()
                            for proj in st.session_state.projects
                        )

                        if not is_duplicate:
                            st.session_state.projects.append({
                                "title": project_title.strip(),
                                "description": project_description.strip()
                            })
                            st.success("Project added successfully!")
                            st.session_state.show_project_form = False  # Hide form after adding
                        else:
                            st.warning("This project already exists in your list.")
                    else:
                        st.warning("Please fill in both the project title and description.")


        # certifications or awards 


        st.subheader("Certifications or Awards")    

        if "certifications" not in st.session_state:
            st.session_state.certifications = []   

        certification_input = st.text_input("Add a Certification or Award")
        
        if st.button("Add Certification or Award"):
            if certification_input:
                
                if certification_input not in [cer.lower() for cer in st.session_state.certifications]:
                    
                    st.session_state.certifications.append(certification_input)
                    
                    st.success(f"'{certification_input}' added to certifications or awards!")
                else:
                    st.warning(f"'{certification_input}' is already in the certifications or awards list.")
        else:
             st.warning("Please enter a certification or award.")      




    # at least one experience should be entered when selected professional resume
            
        

        # Initialize session state
        if "experience" not in st.session_state:
            st.session_state.experience = []

        if "show_experience_form" not in st.session_state:
            st.session_state.show_experience_form = False

        # Show button to add experience
        if st.button("Add Experience"):
            st.session_state.show_experience_form = True

        # Experience form
        if st.session_state.show_experience_form:
            with st.form("experience_form"):
                title = st.text_input("Job Title", placeholder="e.g. Software Engineer")
                company = st.text_input("Company", placeholder="e.g. Google")
                duration = st.text_input("Duration", placeholder="e.g. Jan 2020 - Present")
                bullet_points = st.text_area("Details (one per line)", placeholder="e.g.\n- Developed XYZ\n- Improved performance by 30%")

                submit_exp = st.form_submit_button("Save Experience")

                if submit_exp:
                    if title and company and duration and bullet_points:
                        new_exp = {
                            "title": title.strip(),
                            "company": company.strip(),
                            "duration": duration.strip(),
                            "details": [pt.strip("-• ").strip() for pt in bullet_points.splitlines() if pt.strip()]
                        }

                        if new_exp not in st.session_state.experience:
                            st.session_state.experience.append(new_exp)
                            st.success("Experience added successfully!")
                            st.session_state.show_experience_form = False
                        else:
                            st.warning("This experience already exists.")
                    else:
                        st.warning("Please fill out all fields.")
                        
            




        # Display the filled data in a modern styled format (for visual confirmation)
        st.subheader("Your Resume Preview")
        st.markdown(f"**Name:** {name}")
        st.markdown(f"**City:** {city}")
        st.markdown(f"**State:** {state}")
        st.markdown(f"**Email:** {email}")
        st.markdown(f"**Phone:** {phone}")
        st.markdown(f"**LinkedIn:** {linkedin}")
        st.markdown(f"**Github:** {github}")
        st.markdown(f"**Objective:** {objective}")
        st.markdown(f"**Summary:** {summary}")
        st.markdown(f"**Education:** {degree}, {uni} (Graduation Year: {grad_year})")
        st.markdown(f"**Skills:** {[skill for skill in st.session_state.skills]}" )
        st.markdown("**Projects:**")
        for proj in st.session_state.projects:
             st.markdown(f"- **{proj['title']}**:   {proj['description']}")
        
        st.markdown(f"**Certifications or Awards:** {[cer for cer in st.session_state.certifications]}" ) 


    
        if st.session_state.experience:
            st.markdown("**Current Experience Entries:**")
            for exp in st.session_state.experience:
                st.markdown(f"**{exp['title']} | {exp['company']}**  \n{exp['duration']}")
                for detail in exp['details']:
                    st.markdown(f"- {detail}")
        else:
            st.error("⚠️ Please add at least one experience entry to continue.")

        
        
        # add user input data to a proper data structure 

        resume_data = {
                        
                            "name": name,
                            "city" : city,
                            "state": state,
                
                            "email": email,
                            "phone": phone,
                            "linkedin": linkedin,
                            "github" : github,
                        
                        "objective": objective,
                        "summary": summary,
                        
                          "education":
                          [
                          {
                            "degree": degree,
                            "university": uni,
                            "graduation_year": grad_year
                          },
                          ],
                        "skills": st.session_state.skills,  # list of strings
                        "projects": st.session_state.projects,  # list of {title, description}
                        "certifications": st.session_state.certifications,  # list of strings
                        "experience": [
                            {
                                "title": exp["title"],
                                "company": exp["company"],
                                "duration": exp["duration"],
                                "details": exp["details"]  # list of bullet points
                            }
                            for exp in st.session_state.experience
                        ]
                        
                    }  
        


#-------------------------------------------------------------------------------
       
        
# now , generating resume data for relevant fields

        resume_text = None
        if st.button("✨ Generate Resume"):
            with st.spinner("Generating your optimized resume content..."):
                generated_sections= generate_resume_fields(resume_data,resume_bot_model)

                display_generated_resume(resume_data, generated_sections)

            st.success("✅ Resume generated!")

    
                    

        

def main():

    generate_resume_pdf() 



