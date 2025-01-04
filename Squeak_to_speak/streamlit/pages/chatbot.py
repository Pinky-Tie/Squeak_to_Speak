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

st.title("Squeaky hi")

st.write(f"It's nice to talk to you again, {st.session_state.username}!")

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
