import streamlit as st
import json
from streamlit_lottie import st_lottie
from menu import menu
st.session_state.authentication_status = True
# Redirect to homepage.py if not logged in
menu()
st.set_page_config(layout="wide")
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

with st.container():
    st.header("Gratitude Banner")
    col1, col2, col3,col4,col5 = st.columns(5)
    with col1:
        st.markdown(f':primary-background["Thankful for the sun today!"]')
    with col2:
        st.markdown(f':primary-background["Thankful for my friends listenning to me for hours when I need"]')
    with col3:
        st.markdown(f':primary-background["Finished a new book today. Grateful to all writers"]')
    with col4:
        st.markdown(f':primary-background["Appreciate my morning walk"]')
    with col5:
        st.markdown(f':primary-background["Thankful for hugs"]')
    st.divider()


with st.container():
    col7,col1,col2,col3, col4, col5,col6=st.columns((1,2,2,4,2,2,1))
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
    sp1, coly1, coly2, sp2= st.columns((1, 4, 3, 1))
    with coly1:
        with st.container():
            st.header("Daily Recommendations")
            col1, col2,col3 = st.columns(3)
            with col1:
                st.markdown(f':violet-background["Sleep at least 8 hours every night"]')
            with col2:
                st.markdown(f':green-background["Take a 10-minute walk after meals"]')
            with col3:
                st.markdown(f':blue-background["Limit screen time before bed"]')
            col7, col6, col8, col9 = st.columns((1, 2, 2, 1))
            with col6:
                st.markdown(f':blue-background["Write down your top three priorities for the day"]')
            with col8:
                st.markdown(f':violet-background["Plan your day the night before"]')
    with coly2:
        with st.container():
            st.header("Journal")
            if st.button("""Would you like to make an entry on your journal?  
                        Talk to squeaky!"""):
                st.switch_page("pages/chatbot.py")
