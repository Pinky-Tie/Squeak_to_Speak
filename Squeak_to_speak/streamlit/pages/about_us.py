import streamlit as st
from menu import menu
import json
from streamlit_lottie import st_lottie

# Redirect if neeeded
menu()

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_animation = load_lottiefile("visual_assets\person.json")  

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5, gap="small", vertical_alignment="center")
    with col3:
        st.image(r"visual_assets\ratinho_rosa.png", width=150)
        st.header(''':primary[About us]''')

with st.container():
    col4, col5 = st.columns((2, 1))
    with col4: 
        st.title(":material/crowdsource: Who we are")
        st.markdown("""At ***Squeak to Speak***, we believe that mental health support should be accessible, personalized, and stigma-free.  
                    Our AI-powered assistant uses advanced emotional analysis to offer immediate, customized coping strategies, while also connecting you to the right mental health resources when you're ready.  
                    Whether you're seeking short-term support or long-term therapy, our solution adapts to your needs, making it easier for you to find the help you deserve.  
                    We're here to guide you, every step of the way, towards emotional well-being and the right support - at your own pace.""")
    with col5:
        st_lottie(lottie_animation, speed=1, loop=True, quality="low", height=370, width=370)

with st.container():
    st.divider()
    empty_space, col9, empty_space2 = st.columns((3, 5, 3))
    with col9:
        st.header(''':primary[*Your emotions are unique,*]''')
        st.header(''':primary[*Your support should be too*]''')
    st.divider()

with st.container():
    img, col1 = st.columns((1, 2))
    with col1:
        st.header(':material/history_edu: The Story Behind Squeak to Speak')
        st.markdown('''***Squeak to Speak*** was created with a deep commitment to addressing the silent struggles many face when it comes to mental health. For too long, seeking support has been overshadowed by stigma, uncertainty, and barriers that make accessing the right help feel overwhelming. From the initial hesitation to share emotions to the daunting process of finding a suitable therapist, countless individuals remain trapped in a cycle of avoidance and worsening conditions.  
                    The inspiration for ***Squeak to Speak*** emerged from personal experiences and the stories of others, highlighting a pressing need for a solution that bridges the gap between emotional needs and accessible support. Leveraging the power of large language models (LLMs), we envisioned a tool that could offer understanding, empathy, and guidance.  
                    To close this gap, we built ***Squeaky***, an AI assistant designed to provide more than just temporary relief. ***Squeaky*** empowers users with personalized coping strategies and, when the time is right, connects them with professional help—all while respecting their unique pace, preferences, and financial circumstances.''')
    with img:
        st.image(r"visual_assets\paisagens.png", width=300)
st.divider()

with st.container():
    col6, col7 = st.columns((2, 1))    
    with col7:
        st.header(':material/public: Our Values')
        st.write("""
        :material/mindfulness: Customer-Centricity & Focus
        
        :material/handshake: Respect, Fairness & Empathy
                 
        :material/settings_heart: Integrity & Honesty

        :material/diversity_3: Diversity & Inclusion
                 
        :material/visibility: Transparency & Consistency 
        
        :material/workspace_premium: Quality & Innovation""")
    with col6:
        st.header(':material/diversity_2: Our Team')
        col1, col2,col3,col4 = st.columns((1,3,1,5))
        with col1:
                st.image(r"visual_assets\rato_3.png", width=50)
                st.image(r"visual_assets\rato_4.png", width=50)
                st.image(r"visual_assets\rato_2.png", width=50)
        with col2: 
                st.write("""
                        :material/person_pin: **Joana Sanches**  
                        :material/link: [Linked-in](linkedin.com/in/joana-sanches-15551726b)
                        
                        :material/person_pin: **Margarida Marchão**  
                        :material/link: [Linked-in](linkedin.com/in/mmarchao)
                        
                        :material/person_pin: **Margarida Sardinha**  
                        :material/link: [Linked-in](linkedin.com/in/margaridasardinha)""")
        with col3:
                st.image(r"visual_assets\rato_5.png", width=50)
                st.image(r"visual_assets\rato_1.png", width=50)
        with col4:
            st.write("""  
                    :material/person_pin: **Maria Santos**  
                    :material/link: [Linked-in](linkedin.com/in/maria-l-santos)
                    
                    :material/person_pin: **Renato Bernardino**  
                    :material/link: [Linked-in](linkedin.com/in/renatoroquebernardino)""")
            
