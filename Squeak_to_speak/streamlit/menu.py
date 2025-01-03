import streamlit as st

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/Dashboard.py", label="Your Profile", icon=":material/home:")
    st.sidebar.page_link("pages/chatbot.py", label="Squeaky")
    logout = st.sidebar.button("Logout")
    if logout:
        st.session_state.authentication_status= False
        menu(start=True) 


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("pages/homepage.py", label="Home",icon=":material/home:" )
    st.sidebar.page_link("pages/about_us.py", label="About Squeak to Speak",icon=":material/heart_plus:")
    st.sidebar.page_link("pages/login.py", label="Log in",icon=":material/login:")
 

def menu(start=False, change=False):
    st.logo("visual_assets\Logo_main.png", size="large")
    if start:
       st.switch_page("pages/homepage.py") 
    if change:
        st.switch_page("pages/Dashboard.py")
    if not st.session_state.authentication_status:
        unauthenticated_menu()
        return
    authenticated_menu()

