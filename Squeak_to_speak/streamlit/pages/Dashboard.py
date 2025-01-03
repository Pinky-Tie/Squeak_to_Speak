import streamlit as st

from menu import menu
st.session_state.authentication_status = True
# Redirect to homepage.py if not logged in
menu()


with st.container():
    text1="miau"
    text2="sun"
    text3="rainbows"
    text4="moon"
    col1, col2, col3,col4 = st.columns(4)
    with col1:
        st.markdown(f':primary-background["{text1}"]')
    with col2:
        st.markdown(f':primary-background["{text2}"]')
    with col3:
        st.markdown(f':primary-background["{text3}"]')
    with col4:
        st.markdown(f':primary-background["{text4}"]')
    st.divider()

st.session_state.username="maria"
with st.container():
    col1,col2,col3=st.columns(3)
    with col2:
        st.title(f"Welcome, {st.session_state.username}")