import streamlit as st
import pdfplumber
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#logic
def get_similarity_score(job_description, resume):
    content = [job_description, resume]
    vectorizer = CountVectorizer()
    document_matrix = vectorizer.fit_transform(content)
    similarity_matrix = cosine_similarity(document_matrix)
    match_percentage = similarity_matrix[0][1] * 100
    return round(match_percentage, 2)

def Selection_Tool():
    st.title("Candidate Selection Tool")

    # Job description
    job_description_type = st.radio("Select job description type", ("Upload PDF", "Enter text"))
    if job_description_type == "Upload PDF":
        uploaded_job_description = st.file_uploader("Upload Job Description", type=["pdf", "doc"])
        if uploaded_job_description:
            with pdfplumber.open(uploaded_job_description) as pdf:
                pages = pdf.pages[0]
                job_description = pages.extract_text()
        else:
            job_description = None
    else:
        job_description = st.text_area("Enter job description")

    # Resume
    uploaded_resume = st.file_uploader("Upload resume", type="pdf")
    if uploaded_resume:
        with pdfplumber.open(uploaded_resume) as pdf:
            pages = pdf.pages[0]
            resume = pages.extract_text()
    else:
        resume = None
  
    #button 
    if st.button("Check Matched Score"):
        if job_description or uploaded_job_description:
            if not job_description:
                job_description = uploaded_job_description.read()
            match_percentage = get_similarity_score(job_description, resume)
            st.write("Match Percentage: ", match_percentage, "%")
        else:
            st.warning("Please upload a job description or enter job description text to check the matched score.")
