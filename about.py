import streamlit as st

def About():
        st.subheader("**About The Tool - SMILE RESUME ANALYZER**")

        st.markdown('''

        <p align='justify'>
            A tool which parses information from a resume using natural language processing and finds the keywords, cluster them onto sectors based on their keywords.
            And lastly show recommendations, job role predictions, analytics to the applicant based on keyword matching.
        </p>

        <p align="justify">
            <b>How to use it: -</b> <br/><br/>
            <b>User -</b> <br/>        
            In the Side Bar choose yourself as user and fill the required fields and upload your resume in pdf format.<br/>
            Just sit back and relax our tool will do the magic on it's own.<br/><br/>
            <b>Selection Tools -</b> <br/>           
            check whether a candidate is qualified for a role based his or her education, experience, and other information
            captured on their resume. In a nutshell,its aform of pattern matching between a job s requirements and the qualifications of a
            candidate based on their resume.".<br/><br/>
            <b>Admin -</b> <br/>
            It will load all the required stuffs and perform analysis.
            </p><br/><br/>

        ''',unsafe_allow_html=True)

        with st.expander("Project Members Details", expanded=False):
                st.header("Student Coordinator")
                col1, col2 = st.columns(2)
                with col1:
                     st.subheader("Vishnu Pandey")
                     st.write(" Government Engineering College,Surat"," \n","Email - Vishnupandey9426@gmail.com")
                    
                with col2:
                     st.subheader("Vedanshi Raval")
                     st.write(" L.D. College of Engineering, Ahmedabad"," \n","Email - Ravalvedanshi23@gmail.com")
                
             
    
