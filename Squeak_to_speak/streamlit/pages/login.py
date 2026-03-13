import streamlit as st  
import streamlit_authenticator as stauth  
from menu import menu
from database import users_dict
st.session_state.setdefault("authentication_status", False)
# Redirecting if needed
menu()
st.set_page_config(layout="wide")
st.title("Welcome Back!")


authenticator = stauth.Authenticate(users_dict,
    "ab", "ab", 0)

authenticator.login("main", "Log-in into your account")
name = st.session_state.get("name")
authentication_status = st.session_state.get("authentication_status")
username = st.session_state.get("username")

if authentication_status==False:
    st.error("Incorrect credentials")
    register_button= st.button("Don't have an account yet? Register here!")
    if register_button:
        st.switch_page("pages/user_registration_page.py")

if authentication_status:
    st.success("Login Sucessful")
    st.session_state.authentication_status = True
    st.session_state.username = username
    st.session_state.name = name
    menu(change=True)
if authentication_status==None:
    st.warning("Please enter your email and password")
    register_button= st.button("Don't have an account yet? Register here!")
    if register_button:
        st.switch_page("pages/user_registration_page.py")