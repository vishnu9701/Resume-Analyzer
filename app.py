###### Smile Resume Analyser ######

###### Importing Required Modules ######

import streamlit as st
from streamlit_option_menu import option_menu

###### Importing Required User-Defined Modules ######

from user import NormalUser
from admin import AdminUser
from selection_tool import Selection_Tool
from about import About

@st.cache(suppress_st_warning=True)

def install(package):
    subprocess.check_call([sys.executable, "pip", "install", package])
    

###### Main function run() ######
def main():
    st.set_page_config(
    page_title="AI Resume Analyser",
    page_icon='./Images/mm.png')
    
    selected=option_menu(
        menu_title="RUHVSoft LLP",
        options = ["Resume","Selection-Tool", "About", "Admin"],
        icons=["file-earmark-break","person-bounding-box","person-workspace","gear"],
        menu_icon="emoji-laughing",
        default_index=0,
        orientation="horizontal",)
    
    st.title("AI Resume Analyser")
  

    
    ###### Code for client side (USER) ######

    if selected == 'Resume':
        NormalUser()
        
    elif selected=='Selection-Tool':
        Selection_Tool()

    ###### Code for About Page  ######
        
    elif selected == 'About':
        About()

    ###### Code for Admin Side ######
        
    else:
        AdminUser()
        
        
###### Main Function ######
        
if __name__ == "__main__":
    main()
