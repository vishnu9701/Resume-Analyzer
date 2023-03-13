###### Import Libraries ######
import nltk
nltk.download('stopwords')
import streamlit as st
import pandas as pd
import base64,io,random
import time,datetime
from streamlit_tags import st_tags

###### Libraries for pdf tools ######

from pyresparser import ResumeParser
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter

import nltk
nltk.download('stopwords')

###### Import Courses and  Database File ######

from Courses import resume_videos,interview_videos
from Courses import web_course,soft_course,java_course,py_course,cpp_course,ds_course,test_course,embd_course,dnet_course
from database import ConnectDataBase,CreateDataBase,CreateTable,insert_data
from Courses import web_keyword,soft_keyword,java_keyword,py_keyword,cpp_keyword,ds_keyword,test_keyword,embd_keyword,dnet_keyword

###### Machine Learning Algortihm ######

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer


def get_base64_of_file(file):
    if file is None:
        return None
    else:
        return base64.b64encode(file.read()).decode()

def convert_pdf_to_txt(pdf_file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    for page in PDFPage.get_pages(pdf_file):
        page_interpreter.process_page(page)
    text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
    return text

def course_recommender(course_list):
    st.subheader("**Courses & Certificates Recommendations 👨‍🎓**")
    c = 0
    rec_course = []
    ## slider to choose from range 1-10
    no_of_reco =5
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course


def NormalUser():
    pdf_file = st.file_uploader("Choose your Resume", type=['pdf', 'docx', 'doc'])
    if pdf_file is not None:
        with st.spinner('Hang On While We Cook Magic For You...'):
            time.sleep(3)
        file_bytes = get_base64_of_file(pdf_file)
        st.write(f'<iframe src="data:application/pdf;base64,{file_bytes}" width="600" height="900"></iframe>', unsafe_allow_html=True)
        resume_text = convert_pdf_to_txt(pdf_file)
        resume_data = ResumeParser(pdf_file).get_extracted_data()
        if resume_data:
            st.header("**Resume Analysis 🤘**")
            st.success("Hello "+ resume_data['name'])
            st.subheader("**Your Basic info 👀**")
        
            try:
                st.text('Name: '+resume_data['name'])
                st.text('Email: ' + resume_data['email'])
                st.text('Contact: ' + resume_data['mobile_number'])
            except:
                pass
                
            try:
                st.text('Degree: ' + resume_data['degree'])
            except:
                pass
                
            try:
                st.text('College_Name: ' + resume_data['college_name'])
            except:
                pass
                
            try:
                st.text('Year of Experience' + str(resume_data['total_experience']))
                st.text("Designition" + str(resume_data["designition"]))
            except:
                pass
                    
                  
                ## Predicting Candidate Experience Level 
                
            cand_level = ''
            if resume_data['no_of_pages'] < 1:                
                cand_level = "NA"
                st.markdown( '''<h4 style='text-align: left; color: #d73b5c;'>You are at Fresher level!</h4>''',unsafe_allow_html=True)
                
                #### if internship then intermediate level
                    
            elif 'INTERNSHIP' in resume_text or 'INTERNSHIPS' in resume_text or  'Internship' in resume_text or 'Internships' in resume_text:
                cand_level = "Intermediate"
                st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',unsafe_allow_html=True)

                
                #### if Work Experience/Experience then Experience level
            elif 'EXPERIENCE' in resume_text or 'WORK EXPERIENCE' in resume_text or 'Experience' in resume_text or 'Work Experience'   in resume_text:
                cand_level = "Experienced"
                st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',unsafe_allow_html=True)
            
            else:
                cand_level = "Fresher"
                st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at Fresher level!!''',unsafe_allow_html=True)
                
         
                 ## Skills Analyzing and Recommendation
            st.subheader("**Skills Recommendation 💡**")

            keywords = st_tags(label='### Your Current Skills',
            text='See our skills recommendation below',value=resume_data['skills'],key='1')
                                        ###### Job Role Predication ######

               # Load the job role and skills dataset
            df = pd.read_csv('data.csv')

               # Create a CountVectorizer object to convert job skills to a matrix of token counts
            vectorizer = CountVectorizer(stop_words='english')

               # Fit the vectorizer on the job skills data
            X = vectorizer.fit_transform(df['skills'])

               # Train the Naive Bayes model
            clf = MultinomialNB().fit(X, df['job_role'])
    
            reco_field=clf.predict(vectorizer.transform(resume_data['skills']))[0]
            st.success("** Our analysis says you are looking for Jobs in {} **".format(reco_field))


      

            if reco_field=="Web Development":
                recommended_skills =web_keyword
                recommended_keywords = st_tags(label='### Recommended skills for you.',
                text='Recommended skills generated from System',value=recommended_skills,key = '2')  
                rec_course = course_recommender(web_course)
                
            elif reco_field=="Software Development":
                recommended_skills = soft_keyword
                recommended_keywords = st_tags(label='### Recommended skills for you.',
                text='Recommended skills generated from System',value=recommended_skills,key = '3')
                rec_course = course_recommender(soft_course)
                
            elif reco_field=="Java Developer":
                recommended_skills =java_keyword
                recommended_keywords = st_tags(label='### Recommended skills for you.',
                text='Recommended skills generated from System',value=recommended_skills,key = '4')
                rec_course = course_recommender(java_course)

            elif reco_field=="Python Developer":
                recommended_skills =py_keyword
                recommended_keywords = st_tags(label='### Recommended skills for you.',
                text='Recommended skills generated from System',value=recommended_skills,key = '5')
                rec_course = course_recommender(py_course)
                
            elif reco_field=="C ++ Developer":
                recommended_skills =cpp_keyword
                recommended_keywords = st_tags(label='### Recommended skills for you.',
                text='Recommended skills generated from System',value=recommended_skills,key = '6')
                rec_course = course_recommender(cpp_course)

            elif reco_field=="Data Science":
                recommended_skills =ds_keyword
                recommended_keywords = st_tags(label='### Recommended skills for you.',
                text='Recommended skills generated from System',value=recommended_skills,key = '7')
                rec_course = course_recommender(ds_course)
                
            elif reco_field=="Embedded  System":
                recommended_skills =es_keyword
                recommended_keywords = st_tags(label='### Recommended skills for you.',
                text='Recommended skills generated from System',value=recommended_skills,key = '8')
                rec_course = course_recommender(es_course)
                
            elif reco_field=="DotNet Developer":
                recommended_skills =dnet_keyword
                recommended_keywords = st_tags(label='### Recommended skills for you.',
                text='Recommended skills generated from System',value=recommended_skills,key = '9')
                rec_course = course_recommender(dnet_course)

            elif reco_field=="Software Testing":
                recommended_skills =test_kwyword
                recommended_keywords = st_tags(label='### Recommended skills for you.',
                text='Recommended skills generated from System',value=recommended_skills,key = '10')
                rec_course = course_recommender(test_course)



            # Resume Scorer & Resume Writing Tips
            st.subheader("**Resume Tips & Ideas 🥂**")
            resume_score = 0
                
                ### Predicting Whether these key points are added to the resume

            if 'Education' or 'School' or 'College'  in resume_text:
                resume_score = resume_score + 15
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Education Details</h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Education. It will give Your Qualification level to the recruiter</h4>''',unsafe_allow_html=True)

            if 'EXPERIENCE' in resume_text or 'Experience' in resume_text:
                resume_score = resume_score + 15
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Experience</h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Experience. It will help you to stand out from crowd</h4>''',unsafe_allow_html=True)

            if 'INTERNSHIPS'  in resume_text or 'INTERNSHIP' in resume_text or 'Internships' in resume_text or 'Internship' in resume_text or 'Intern' in resume_text or 'INTERN' in resume_text:
                resume_score = resume_score + 9
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Internships</h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Internships. It will help you to stand out from crowd</h4>''',unsafe_allow_html=True)

            if 'SKILLS'  in resume_text or 'SKILL' in resume_text or 'Skills'  in resume_text or 'Skill' in resume_text :
                resume_score = resume_score + 6
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Skills</h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Skills. It will help you a lot</h4>''',unsafe_allow_html=True)
                    
            if 'PROJECTS' in resume_text or 'PROJECT' in resume_text or 'Projects' in resume_text or 'Project' in resume_text:
                resume_score = resume_score + 15
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Projects. It will show that you have done work related the required position or not.</h4>''',unsafe_allow_html=True)


            if 'HOBBIES' in resume_text or 'Hobbies' in resume_text or 'INTERESTS' in resume_text or 'SOFT'in resume_text or 'Soft' in resume_text or 'GOAL' in resume_text or 'Goal' in resume_text :
                resume_score = resume_score + 6
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies/Interests</h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Hobbies/Intrests. It will show your personality to the Recruiters and give the assurance that you are fit for this role or not.</h4>''',unsafe_allow_html=True)
                

            if 'ACHIEVEMENTS' in resume_text or 'Achievements' in resume_text or 'Achievement' in resume_text or 'ACHIEVEMENT' in resume_text or 'Awards' in resume_text or 'AWARD' in resume_text :
                resume_score = resume_score + 9
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements </h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Achievements. It will show that you are capable for the required position.</h4>''',unsafe_allow_html=True)

            if 'CERTIFICATIONS' in resume_text or 'Certifications' in resume_text or 'Certification' in resume_text  or 'CERTIFICATES' in resume_text or 'CERTIFICATE' in resume_text or 'Certificate' in resume_text or 'Certficates' in resume_text :
                resume_score = resume_score + 9
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Certifications </h4>''',unsafe_allow_html=True)
 
            else:
                st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Certifications. It will show that you have done some specialization for the required position.</h4>''',unsafe_allow_html=True)

                
            if 'LANGUAGES' in resume_text or 'Language' in resume_text or 'Languages' in resume_text:
                resume_score = resume_score + 6
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Languages </h4>''',unsafe_allow_html=True)
 
            else:
                st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please Menation Languages you know. It will show that you have diffrent communication skills.</h4>''',unsafe_allow_html=True)

            if 'SUMMARY'in resume_text or 'Summary' in resume_text or 'OBJECTIVES' in resume_text or 'Objectives' in resume_text or 'Objective' in resume_text:
                resume_score = resume_score + 3
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Summary/Objective</h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Summary/Objective. It will show your single word presentation to the comapny.</h4>''',unsafe_allow_html=True)

            if 'LEADERSHIP'in resume_text or 'Leadership' in resume_text or 'VOLUNTEER' in resume_text or 'Volunteer' in resume_text or 'Volunteers' in resume_text:
                resume_score = resume_score + 6
                st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Summary/Objective</h4>''',unsafe_allow_html=True)
            else:
                st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Leadership/Volunteer. It will show your Leadership & Managnement skiils to the comapny.</h4>''',unsafe_allow_html=True)
            st.subheader("**Resume Score 📝**")
                
            st.markdown(
                    """
                    <style>
                        .stProgress > div > div > div > div {
                            background-color: #d73b5c;
                        }
                    </style>""",
                    unsafe_allow_html=True,
                )

                ### Score Bar
            my_bar = st.progress(0)
            score = 0
            for percent_complete in range(resume_score):
                score +=1
                time.sleep(0.03)
                my_bar.progress(percent_complete + 1)

     
            st.success('** Your Resume Writing Score: ' + str(score)+'**')
            st.warning("** Note: This score is calculated based on the content that you have added in your Resume. **")
            ts = time.time()
            cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            timestamp = str(cur_date+'_'+cur_time)
            
            insert_data(resume_data['name'],resume_data['email'],resume_data['mobile_number'],str(resume_score),
                        str(cand_level),reco_field,str(resume_data['skills']),timestamp)
           
            
            st.balloons()

