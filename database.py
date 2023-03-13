import streamlit as st
import pymysql

####### Sql connector ######

def ConnectDataBase():
    connection = pymysql.connect.connect(**st.secrets["db_credentials"])

    #connection = pymysql.connect(host="localhost",user="root",password="vedu",db='cv')
    cursor = connection.cursor()
    return connection, cursor


###### Creating Database ######
    
def CreateDataBase():
    connection, cursor = ConnectDataBase()
    cursor.execute("""CREATE DATABASE IF NOT EXISTS CV;""")
        
###### Creating Table user-data ######

def CreateTable():
    connection, cursor = ConnectDataBase()  

    
# (name,email,mobile,res_score,cand_level,skills,timestamp)

    DB_table_name = 'user_data'
    table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                    Name varchar(500) NOT NULL,
                    Email_ID VARCHAR(500) NOT NULL,
                    Mobile_No VARCHAR(15) NOT NULL,
                    resume_score VARCHAR(8) NOT NULL,
                    User_level VARCHAR(30) NOT NULL,
                    Predicted_Field VARCHAR(60) NOT NULL,
                    Actual_skills VARCHAR(1200) NOT NULL,
                    Timestamp VARCHAR(50) NOT NULL,
                    PRIMARY KEY (ID)
                    );
                """
    cursor.execute(table_sql)


###### Insertng Data into Database Table ######

# (name,email,mobile,res_score,cand_level,reco_field,skills,rate,timestamp)


def insert_data(name,email,mobile,res_score,cand_level,reco_field,skills,timestamp):
    connection, cursor = ConnectDataBase()
    DB_table_name = 'user_data'
    insert_sql = "insert into " + DB_table_name + """
    values (0,%s,%s,%s,%s,%s,%s,%s,%s)"""
    rec_values = (name,email,mobile,str(res_score),cand_level,reco_field,skills,timestamp)
    cursor.execute(insert_sql, rec_values)
    connection.commit()


