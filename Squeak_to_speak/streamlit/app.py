import streamlit as st
from menu import menu
import sys
import os
from pathlib import Path

# Add the Squeak_to_speak root directory to sys.path
project_root = Path(__file__).resolve().parents[2]  # Go up two levels to the root
sys.path.append(str(project_root))

st.set_page_config(layout="wide")
st.logo("visual_assets\Logo_main.png", size="large")


# Initialize st.session_state.authentication_status to False
st.session_state.authentication_status = True
st.session_state.username = "gabriel.hernandez9@outlook.com"
st.session_state.name = "gabriel"

#st.session_state.authentication_status= False
menu(change=True) 
