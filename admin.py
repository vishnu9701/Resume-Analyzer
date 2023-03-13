import streamlit as st
import pandas as pd
import base64,random
import pymysql
import plotly.express as px
from database import ConnectDataBase

def to_1D(series):
    return pd.Series([x.replace('[', '').replace(']', '') for _list in series for x in _list.split(", ")])

def AdminUser():
    ## Admin Side
        
        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')
        if st.button('Login'):
            if ad_user == 'admin' and ad_password == '123':
                st.success("Welcome Admin")
                st.write('''<b>Vistors</b> <img src="https://counter4.optistats.ovh/private/freecounterstat.php?c=baukt6rkh7fz3ee4l3r9g31b29hrmq17"
                             border="0"></a> 
                         ''', unsafe_allow_html=True)
                

                # Display Data
                connection, cursor=ConnectDataBase()
                
                cursor.execute('''SELECT*FROM user_data''')
                data = cursor.fetchall()
                st.header("**User's👨‍💻 Data**")
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email','Mobile_No', 'Resume Score','User Level','Predicted_Field','Actual Skills', 'Timestamp'])
                st.dataframe(df)
                st.markdown(get_csv_download_link(df,'User_Data.csv','Download Report'), unsafe_allow_html=True)
                
                ## Admin Side Data
                query = 'select * from user_data;'
                plot_data = pd.read_sql(query, connection)

                

                ### Pie chart for User's👨‍💻 Experienced Level
                labels = plot_data.User_level.unique()
                values = plot_data.User_level.value_counts()
                st.subheader("📈 ** Pie-Chart for User's👨‍💻 Experienced Level**")
                fig = px.pie(df, values=values, names=labels, title="Pie-Chart📈 for User's👨‍💻 Experienced Level")
                st.plotly_chart(fig)

                 # fetching resume_score from the query and getting the unique values and total value count                 
                labels = plot_data.resume_score.unique()                
                values = plot_data.resume_score.value_counts()

                # Pie chart for Resume Score
                st.subheader("**Pie-Chart for Resume Score**")
                fig = px.pie(df, values=values, names=labels, title='From 1 to 100 💯', color_discrete_sequence=px.colors.sequential.Agsunset)
                st.plotly_chart(fig)

                # fetching Predicted_Field from the query and getting the unique values and total value count                 
                labels = plot_data.Predicted_Field.unique()
                values = plot_data.Predicted_Field.value_counts()

                # Pie chart for predicted field recommendations
                st.subheader("**Pie-Chart for Predicted Field Recommendation**")
                fig = px.pie(df, values=values, names=labels, title='Predicted Field according to the Skills 👽', color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
                st.plotly_chart(fig)

                st.subheader("📈 **Bar-Chart📈 for User's 🛠️ Skills**")
                d = to_1D(plot_data["Actual_skills"]).value_counts()
                d = pd.DataFrame({'skill': d.index, 'count': d.values})
                fig = px.bar(d, x="skill", y="count",
                             title="Bar-Chart📈 for User's 🛠️ Skills")
                st.plotly_chart(fig)


            else:
                st.error("Wrong ID & Password Provided")


def get_csv_download_link(df,filename,text):
    csv = df.to_csv(index=False)
    ## bytes conversions
    b64 = base64.b64encode(csv.encode()).decode()      
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href
