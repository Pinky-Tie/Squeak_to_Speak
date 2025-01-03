import streamlit as st
from menu import menu
import sys
import os


# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

st.set_page_config(layout="wide")
st.logo("visual_assets\Logo_main.png", size="large")


# Initialize st.session_state.authentication_status to False


st.session_state.authentication_status= True
st.session_state.username = "Maria"
menu(change=True) 
