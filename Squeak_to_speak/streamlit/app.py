import streamlit as st
from menu import menu
import sys
import os
st.set_page_config(layout="wide")
st.logo("visual_assets\Logo_main.png", size="large")

# Initialize st.session_state.authentication_status to False
st.session_state.authentication_status= False
menu(start=True)