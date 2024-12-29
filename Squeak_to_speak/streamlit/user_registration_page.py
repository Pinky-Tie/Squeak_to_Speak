import datetime
import re
import sqlite3

import streamlit as st

from users_db import UserDatabase

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


db_path = "ecommerce.db"
conn = sqlite3.connect(db_path)
db = UserDatabase(conn)

st.title("User Registration")

with st.form("registration_form"):
    col1, col2 = st.columns(2)

    with col1:
        first_name = st.text_input("First Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        address = st.text_area("Address")

    with col2:
        last_name = st.text_input("Last Name")
        password = st.text_input("Password", type="password")
        gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
        dob = st.date_input(
            "Date of Birth",
            min_value=datetime.date(1900, 1, 1),
            max_value=datetime.date.today(),
        )

        submit = st.form_submit_button("Register")

    if submit:
        if (
            not all([first_name, last_name, phone, address, email, password])
            or gender == "Select"
        ):
            st.error("Please fill all fields")
            st.session_state.register_in = False
        elif not is_valid_email(email):
            st.error("Please enter a valid email")
            st.session_state.register_in = False
        elif len(password) < 8:
            st.error("Password must be at least 8 characters")
            st.session_state.register_in = False
        elif db.check_if_email_exists(email):
            st.error("Email already registered")
            st.session_state.register_in = False
        else:
            if db.add_user(
                first_name, last_name, email, password, phone, address, gender, dob
            ):
                st.success("Registration Successful!")
                st.session_state.register_in = True
            else:
                st.error("Registration failed. Please try again.")
                st.session_state.register_in = False
        st.rerun()