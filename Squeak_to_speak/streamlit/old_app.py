import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dotenv import load_dotenv  # Import dotenv to load environment variables
from chatbot.bot import MainChatbot  # Import the chatbot class
import streamlit as st
import time


def main(bot: MainChatbot):
    """Main interaction loop for the chatbot.

    Args:
        bot: An instance of the MainChatbot.
    """


    while True:
        # Prompt the user for input
        user_input = input("You: ").strip()

        # Allow the user to exit the conversation
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        try:
            # Process the user's input using the bot and display the response
            response = bot.process_user_input({"customer_input": user_input})
            print(f"Bot: {response}")
        except Exception as e:
            # Handle any exceptions and prompt the user to try again
            print(f"Error: {str(e)}")
            print("Please try again with a different query.")

def display_rotating_banner(bot):
    """
    Displays a rotating banner of random gratitude messages.
    """
    placeholder = st.empty()
    while True:
        random_gratitude_message = bot.get_random_gratitude_message()
        placeholder.text(random_gratitude_message)
        time.sleep(5)  # Rotate every 5 seconds

if __name__ == "__main__":
    # Load environment variables from a .env file
    load_dotenv()

    # Notify the user that the bot is starting
    print("Starting the bot...")


    user_id = input("Enter your user ID: ").strip()

    #This value is not stored on the database, needing value only to satisfy langchains memory functions, as such, it is hardcoded to 1
    conversation_id = 1
    # Initialize the CustomerServiceBot with dummy user and conversation IDs
    bot = MainChatbot(user_id=int(user_id), conversation_id=conversation_id)
    

    # Display instructions for ending the conversation
    print("Bot initialized. Type 'exit' or 'quit' to end the conversation.")

    # Display the rotating banner of random gratitude messages
    '''st.title("Rotating Banner of Gratitude Messages")
    display_rotating_banner(bot)'''

    # Start the main interaction loop
    main(bot)

'''def Homepage():
    st.title("Homepage")

pg = st.navigation([st.Page(Homepage), st.Page("login_page.py"), st.Page("user_registration.py")])
pg.run()
'''