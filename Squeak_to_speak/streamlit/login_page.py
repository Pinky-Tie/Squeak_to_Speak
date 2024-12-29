import sqlite3

import streamlit as st
from users_db import UserDatabase


def load_database():
    return sqlite3.connect("ecommerce.db")

conn = load_database()
db = UserDatabase(conn)

st.title("Login")

with st.form("login_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

    if submit:
        if not email or not password:
            st.error("Please fill all fields")
            st.session_state.logged_in = False
        elif not db.check_if_email_exists(email):
            st.error("Email not registered")
            st.session_state.logged_in = False
        elif not db.verify_user(email, password):
            st.error("Incorrect password")
            st.session_state.logged_in = False
        else:
            st.success("Login successful!")
            # Get user details and store in session state
            st.session_state.user_details = db.get_user_details(email)
            st.session_state.logged_in = True
        st.rerun()