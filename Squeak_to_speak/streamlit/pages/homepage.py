import streamlit as st
from menu import menu
import json
from streamlit_lottie import st_lottie

# Redirect if needed
menu()


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_animation = load_lottiefile("visual_assets\hands.json")  
lottie_animation2 = load_lottiefile("visual_assets\heart.json")  

with st.container():
    col1, col2,col3= st.columns((4,8,1))
    with col2:
        st.image(r"visual_assets\Logo__pb.png", width=400)

with st.container():
    col4, col5 = st.columns((2, 1))
    with col4: 
        st.title(":material/Frame_Person: Get the mental health support that fits YOU")
        st.markdown("""Discover personalized AI-powered mental health support tailored to your needs and goals.  
                    Whether you're looking for temporary strategies or a path to long-term emotional well-being, we're here for you.""")
        register_now = st.button("Join us now!")
        if register_now:
            st.switch_page("pages/user_registration_page.py")
    with col5:
        st_lottie(lottie_animation, speed=1, loop=True, quality="low", height=270, width=270)

with st.container():
    st.divider()
    st.title(":material/person_raised_hand: Why Squak to Speak?")
    col6, col7, col8,col9 = st.columns(4)
    with col6:
        col1,col2,col3=st.columns((3,4,4))
        with col2:
            st.image(r"visual_assets\icon1.png", width=150)
        st.markdown('''**Personalized Emotional Support**''')
        st.markdown('''Our AI understands your unique emotions and tailors its support to match your needs and pace.''')
    with col7:
        col1,col2,col3=st.columns((2,4,5))
        with col2:
            st.image(r"visual_assets\icon2.png", width=150)
        st.markdown('''**Adapted Coping Strategies**''')
        st.markdown('''Receive practical, easy-to-implement strategies that fit seamlessly into your daily life.''')
    with col8:
        col1,col2,col3=st.columns((4,5,5))
        with col2:
            st.image(r"visual_assets\icon3.png", width=150)
        st.markdown('''**Connection with Professionals**''')
        st.markdown('''When you're ready, our platform helps you find a therapist or counselor perfectly suited to your personality, preferences, and availability.''')
    with col9:
        col1,col2,col3=st.columns((3,4,4))
        with col2:
            st.image(r"visual_assets\icon4.png", width=150)
        st.markdown('''**24/7 Availability**''')
        st.markdown('''Access support whenever you need it, with complete privacy and security''')
   


with st.container():
    st.divider()
    st.title(":material/crowdsource: Testimonials")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(''':primary-background["I was hesitant to seek therapy, but Squeak to Speak helped me take the first step. The AI's coping strategies were so helpful, and it matched me with a therapist who truly gets me."  
                    Anna P.]''')
    with col2:
        st.markdown(''':primary-background["The personalized advice I received gave me the confidence to make small, positive changes in my daily routine. I've never felt so understood."  
                    James R.]''')
    with col3:
        st.markdown(''':primary-background["Having someone to talk to 24/7 has been a game-changer. I no longer feel alone."  
                    Marta S.]''')

with st.container():
    st.divider()
    col4, space2 = st.columns((5,3))
    with col4:
        st.header(''':primary[Ready to Start Your Journey?]''')
        st.markdown("""Take the first step toward understanding your emotions and finding the support you deserve.  
                    Let Squeak to Speak guide you.""")
        register_now = st.button("Sing Up Now")
        if register_now:
            st.switch_page("pages/user_registration_page.py")
    st.divider()
    with space2:
        st.image(r"visual_assets\logo_pretty.png", width=450)

with st.container():
    col1, col2, col3, col4= st.columns(4)
    with col1:
        st.image(r"visual_assets\s1.png", width=350)
    with col2:
        st.image(r"visual_assets\s2.png", width=350)
    with col3:
        st.image(r"visual_assets\s3.png", width=350)
    with col4:
        st.image(r"visual_assets\s4.png", width=350)
