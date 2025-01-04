import streamlit as st
import json
from streamlit_lottie import st_lottie
from Squeak_to_speak.data.data_func import get_jornal_entries
from Squeak_to_speak.data.data_func import gratitude_comments
from Squeak_to_speak.data.daily_rec import select_random_habits
from menu import menu
st.session_state.authentication_status = True
# Redirect to homepage.py if not logged in
menu()

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

with st.container():
    st.divider()
    st.header("Gratitude Banner")
    random_comments = gratitude_comments()
    col1, col2, col3,col4,col5 = st.columns(5)
    with col1:
        st.markdown(f':primary-background["{random_comments[0]}"]')
    with col2:
        st.markdown(f':primary-background["{random_comments[1]}"]')
    with col3:
        st.markdown(f':primary-background["{random_comments[2]}"]')
    with col4:
        st.markdown(f':primary-background["{random_comments[3]}"]')
    with col5:
        st.markdown(f':primary-background["{random_comments[4]}"]')
    st.divider()


with st.container():
    col1,col2,col7,col3,col6, col4, col5=st.columns((2,2,1,5,1,2,2))
    with col1:
        st_lottie(load_lottiefile("visual_assets\e1.json"), speed=1, loop=True, quality="low", height=100, width=100)
    with col2:
        st_lottie(load_lottiefile("visual_assets\e2.json"), speed=1, loop=True, quality="low", height=100, width=100)
    with col5:
        st_lottie(load_lottiefile("visual_assets\e3.json"), speed=1, loop=True, quality="low", height=100, width=100)
    with col4:
        st_lottie(load_lottiefile("visual_assets\e4.json"), speed=1, loop=True, quality="low", height=100, width=100)
    with col3:
        st.header(f":primary[Welcome, {st.session_state.name}]")

with st.container():
    st.divider()
    col4, col5= st.columns(2)
    with col4:
        st.header("Daily Recommendations")
        habits=select_random_habits()
        col1, col2,col3 = st.columns(3)
        with col1:
            st.markdown(f':violet-background["{habits[0]}"]')
        with col2:
            st.markdown(f':green-background["{habits[1]}"]')
        with col3:
            st.markdown(f':blue-background["{habits[2]}"]')
        col4, col6 = st.columns(2)
        with col4:
            st.markdown(f':blue-background["{habits[3]}"]')
        with col6:
            st.markdown(f':violet-background["{habits[4]}"]')
    with col5:
        st.header("Journal")
        journal_entry = get_jornal_entries(st.session_state.username)
        if journal_entry:
            st.markdown(f':grey-background["{journal_entry[0]}"]')
        else:
            if st.button("""Would you like to make an entry on your journal?  
                         Talk to squeaky!"""):
                st.switch_page("pages/chatbot.py")
