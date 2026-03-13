import streamlit as st
from menu import menu
import os
import sys
import random
import time
st.session_state.authentication_status = True
# Redirect to homepage.py if not logged in
menu()
st.set_page_config(layout="wide")
@st.dialog("Discover how to benefit from Squeaky")
def show_help():
    col1, col2=st.columns((3,4))
    with col1:
        st.markdown("""**Intention**""") 
    with col2:
        st.markdown("""**Start your message with**""") 
    st.divider()
    st.markdown(""":primary-background[Journal]""") 

    col1, col2=st.columns((2,4))
    with col1:
        st.markdown("""Insert an entry  
                    Update an entry  
                    Delete an entry  
                    View an entry  
                    Chat about an entry""")
    with col2:
        st.markdown(""""I want to add to my journal today: …"  
                    "I want to change a journal entry"  
                    "Delete my journal entry on…"  
                    "How was my day on…"  
                    "I want to talk about how I felt on…"
""") 
    st.divider()
    st.markdown(""":primary-background[Mood Board]""") 

    col1, col2=st.columns((3,4))
    with col1:
        st.markdown("""Insert Mood Board Entry  
                    Update Mood Board Entry  
                    Delete Mood Board Entry  
                    View Mood Board Entry""") 
    with col2:
        st.markdown(""""Today, I feel..."  
                    "I want to change my mood..."  
                    "Delete my mood on..."  
                    "How did I feel on..."
""") 
    st.divider()
    st.markdown(""":primary-background[Gratitude Banner]""") 

    col1, col2=st.columns((3,4))
    with col1:
        st.markdown("""Insert Gratitude Entry""") 
    with col2:
        st.markdown(""" "I am grateful for..." """) 
    st.divider()
    st.markdown(""":primary-background[Find Help]""") 

    col1, col2=st.columns((3,4))
    with col1:
        st.markdown("""Find a Therapist  
                    Find a Support Group  
                    Find a Hotline  
                    Find a habit alternative""") 
    with col2:
        st.markdown(""""Help me find a therapist that..."  
                    "Help me find a support group that..."  
                    "Help me find a hotline that..."  
                    "Suggest an alternative for..."
""") 
    st.divider()
    st.markdown(""":primary-background[About us]""") 

    col1, col2=st.columns((3,4))
    with col1:
        st.markdown("""Learn about us  
                    Learn about Squeaky
                    Review your data""") 
    with col2:
        st.markdown(""""Tell me about Squeak to Speak"  
                    "Tell me about your chatbot"  
                    "What data do you have on me?"
""") 

col1, col2 = st.columns((8,1))
with col1: 
    st.title("Squeaky")
    st.warning("DEMO VERSION: Squeaky main version is currently unavailable for use.   Feel free to explore an echo demo version available.")

with col2:
    if st.button("Discover how to benefit from Squeaky"):
        show_help()

if "messages" not in st.session_state:
        st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar", None)):
        st.markdown(message["content"])

prompt = st.chat_input("How are you feeling today?")
if prompt:
    with st.chat_message("user", avatar="visual_assets/Pessoa.png"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "visual_assets/Pessoa.png"})

    response = prompt
    with st.chat_message("assistant",  avatar="visual_assets/Ratinho.png"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response, "avatar": "visual_assets/Ratinho.png"})

