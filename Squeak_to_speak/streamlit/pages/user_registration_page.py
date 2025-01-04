import re
import streamlit as st
from Squeak_to_speak.data.data_func import is_email_unique, add_user
from menu import menu

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

st.title("User Registration")

empty_space, button_place = st.columns((18, 1))
with button_place: 
    if st.button("", type="tertiary", icon=":material/close:"):
        st.switch_page("pages/homepage.py")

with st.form("registration_form"):
    name = st.text_input("Name")
    username = st.text_input("Email")
    country = st.text_input("Country")
    password = st.text_input("Password", type="password")

    submit = st.form_submit_button("Register")

    if submit:
        if (
            not all([name, username, country, password])):
            st.error("Please fill all fields")
            st.session_state.authentication_status = False
        elif not is_valid_email(username):
            st.error("Please enter a valid email")
            st.session_state.authentication_status = False
        elif len(password) < 8:
            st.error("Password must be at least 8 characters")
            st.session_state.authentication_status = False
        elif not is_email_unique(username):
            st.error("Email already registered")
            st.session_state.authentication_status = False
        else:
            if add_user(name, username, password, country):
                st.success("Registration Successful!")
                st.session_state.authentication_status = True
                st.session_state.username = username
                st.session_state.name = name
                menu(change=True)
            else:
                st.error("Registration failed. Please try again.")
                st.session_state.authentication_status = False
                menu(start=True)