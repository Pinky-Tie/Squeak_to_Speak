import streamlit as st  
import streamlit_authenticator as stauth  
from streamlit_option_menu import option_menu
from menu import menu
from Squeak_to_speak.data.data_func import retrieve_data

# Redirecting if needed
menu()

st.title("Welcome Back!")

st.session_state.authentication_status = None

# Retrieving data
user_data= retrieve_data()
usernames=user_data["email"]
names = user_data["username"]
hashed_passwords = stauth.Hasher(user_data["password"]).generate()

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "ab", "ab", cookie_expiry_days=0)

name, authentication_status, username = authenticator.login("Log-in into your account", "main")

if authentication_status==False:
    st.error("Incorrect credentials")
    register_button= st.button("Don't have an account yet? Register here!")
    if register_button:
        st.switch_page("pages/user_registration_page.py")

if authentication_status:
    st.success("Login Sucessful")
    st.session_state.authentication_status = True
    st.session_state.username = name
    menu(change=True)
if authentication_status==None:
    st.warning("Please enter your email and password")
    register_button= st.button("Don't have an account yet? Register here!")
    if register_button:
        st.switch_page("pages/user_registration_page.py")