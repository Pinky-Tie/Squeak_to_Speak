import streamlit as st
from openai import OpenAI
from menu import menu
from dotenv import load_dotenv  # Import dotenv to load environment variables
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from Squeak_to_speak.chatbot.bot import MainChatbot
load_dotenv()


# Redirect to homepage.py if not logged in
menu()

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

col1, col2 = st.columns((6,2))
with col1: 
    st.title("Squeaky")
with col2:
    if st.button("Discover how to benefit from Squeaky"):
        show_help()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

def main(user_input):
    """Main interaction loop for the chatbot.

    Args:
        bot: An instance of the MainChatbot.
    """
    try:
        bot= MainChatbot()
        # Process the user's input using the bot and display the response
        response = bot.process_user_input({"customer_input": prompt})
        print(f"Response type: {type(response)}")
        return response

    except Exception as e:
        # Handle any exceptions and prompt the user to try again
        response=(f"Error: {str(e)}")
        return response


if __name__ == "__main__":
    # Load environment variables from a .env file
    load_dotenv()

    # Notify the user that the bot is starting
    print("Starting the bot...")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(name=message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])

prompt= st.chat_input("What is on your mind?")
# React to user input
if prompt:
    with st.chat_message(name="user", avatar="visual_assets\Pessoa.png"):
        st.markdown(prompt)
        response = main(prompt) 
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar":"visual_assets\Pessoa.png"}) 
    # Display assistant response in chat message container
    with st.chat_message(name="assistant", avatar="visual_assets\Ratinho.png"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response, "avatar":"visual_assets\Ratinho.png"})
