# Import necessary classes and modules for chatbot functionality
import sys
import os

from chatbot.chains.review_user_memory import UserInteractionHandler, UserQueryChain, UserResponseChain
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import re

from typing import Callable, Dict, Optional, List, Union
from dateutil.parser import parse

from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from chatbot.memory import MemoryManager
from chatbot.router.loader import load_intention_classifier

from data.database_functions import DatabaseManager
from chatbot.rag import RAGPipeline

from chatbot.chains.chitchat import ChitChatClassifierChain, ChitChatResponseChain
from chatbot.chains.delete_journal import JournalEntryDeleter, DeletionConfirmationFormatter
from chatbot.chains.delete_mood import MoodBoardEntryDeleter, MoodBoardDeletionConfirmationFormatter
from chatbot.chains.insert_gratitude import GratitudeEntryManager, GratitudeEntryResponse
from chatbot.chains.insert_journal import JournalEntryManager, JournalEntryResponse
from chatbot.chains.insert_mood import MoodEntryManager, MoodEntryResponse
from chatbot.chains.update_journal import IdentifyJournalEntryToModify, ModifyJournalEntry, InformUserOfJournalChange
from chatbot.chains.update_mood import IdentifyMoodBoardEntryToModify, ModifyMoodBoardEntry, InformUserOfMoodBoardChange
from chatbot.chains.view_journal import JournalInteractionHandler, JournalQueryChain, JournalResponseChain
from chatbot.chains.view_mood import MoodInteractionHandler, MoodQueryChain, MoodResponseChain

#databse connection
import sqlite3

db_file = 'Squeak_to_speak\data\Squeaktospeak_db.db'

conn = sqlite3.connect(db_file, check_same_thread= False)
db_manager = DatabaseManager(conn)


class MainChatbot:
    """A bot that handles customer service interactions by processing user inputs and
    routing them through configured reasoning and response chains.
    """

    def __init__(self, user_id: int, conversation_id: int):
        """Initialize the bot with session and language model configurations."""
        # Initialize the memory manager to manage session history
        self.memory = MemoryManager()

        # Configure the language model with specific parameters for response generation
        self.llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini")
        self.db_manager = DatabaseManager(conn)

        self.user_id = user_id
        self.conversation_id = conversation_id
        self.memory_config = {
            "configurable": {
                "user_id": self.user_id,
                "conversation_id": self.conversation_id,
            }
        }

        self.rag = self.add_memory_to_runnable(
            RAGPipeline(
                index_name="pdf-data",
                embeddings_model="text-embedding-3-small",
                llm=self.llm,
                memory=True,
            ).rag_chain
        )
        

        # Initialize handlers for each intent
        self.mood_board_entry_deleter = MoodBoardEntryDeleter(db_manager=self.db_manager)
        self.mood_board_deletion_confirmation_formatter = MoodBoardDeletionConfirmationFormatter()
        
        self.journal_entry_deleter = JournalEntryDeleter(db_manager=self.db_manager)
        self.deletion_confirmation_formatter = DeletionConfirmationFormatter()

        self.journal_manager = JournalEntryManager(db_manager=self.db_manager)
        self.journal_entry_response = JournalEntryResponse()
        

        self.gratitude_manager = GratitudeEntryManager(db_manager=self.db_manager)
        self.gratitude_entry_response = GratitudeEntryResponse()

        self.mood_manager = MoodEntryManager(db_manager=self.db_manager)
        self.mood_entry_response = MoodEntryResponse()

        self.identify_mood_board_entry_to_modify = IdentifyMoodBoardEntryToModify()
        self.modify_mood_board_entry = ModifyMoodBoardEntry(db_manager=self.db_manager)
        self.inform_user_of_mood_board_change = InformUserOfMoodBoardChange()

        self.identify_journal_entry_to_modify = IdentifyJournalEntryToModify()
        self.modify_journal_entry = ModifyJournalEntry(db_manager=self.db_manager)
        self.inform_user_of_journal_change = InformUserOfJournalChange()

        self.chitchat_classifier_chain = ChitChatClassifierChain(llm=self.llm)
        self.chitchat_response_chain = self.add_memory_to_runnable(ChitChatResponseChain(llm=self.llm))
        
        # Map of intentions to their corresponding chains
        # Map intent names to their corresponding reasoning and response chains
        self.chain_map = {
            "delete_mood": {
                "delete": self.mood_board_entry_deleter,
                "confirm": self.mood_board_deletion_confirmation_formatter
            },
            "delete_journal": {
                "delete": self.journal_entry_deleter,
                "confirm": self.deletion_confirmation_formatter
            },
            "insert_mood": {
                "insert": self.mood_manager,
                "response": self.mood_entry_response
            },
            "insert_journal": {
                "insert": self.journal_manager,
                "response": self.journal_entry_response
            },
            "insert_gratitude": {
                "insert": self.gratitude_manager,
                "response": self.gratitude_manager
            },
            "update_mood": {
                "identify": self.identify_mood_board_entry_to_modify,
                "modify": self.modify_mood_board_entry,
                "inform": self.inform_user_of_mood_board_change
            },
            "update_journal": {
                "identify": self.identify_journal_entry_to_modify,
                "modify": self.modify_journal_entry,
                "inform": self.inform_user_of_journal_change
            },
            "chitchat": {
                "reasoning": self.chitchat_classifier_chain,
                "response": self.chitchat_response_chain
            }
        }
        self.chitchat_classifier_chain = ChitChatClassifierChain(llm=self.llm)
        self.chitchat_response_chain = self.add_memory_to_runnable(ChitChatResponseChain(llm=self.llm))


        # Map of intentions to their corresponding handlers
        self.intent_handlers: Dict[Optional[str], Callable[[Dict[str, str]], str]] = {
        "find_therapist": self.handle_find_therapist,
        "find_support_group": self.handle_find_support_group,
        "find_hotline": self.handle_find_hotline,
        "habit_alternatives": self.handle_habit_alternatives,
        "insert_mood": self.handle_insert_mood,
        "insert_journal": self.handle_insert_journal,
        "insert_gratitude": self.handle_insert_gratitude,
        "ask_missionvalues": self.handle_know_mission,
        "ask_features": self.handle_know_services,
        "update_journal": self.handle_update_journal,
        "update_mood": self.handle_update_mood,
        "delete_journal":self.handle_delete_journal,
        "delete_mood":self.handle_delete_mood,
        'chitchat':self.handle_chitchat_intent,
        'view_journal':self.handle_view_journal,
        'view_mood':self.handle_view_mood,
        "review_user_memory": self.handle_review_user_memory,
        }
        # Load the intention classifier to determine user intents
        self.intention_classifier = load_intention_classifier()


    def add_memory_to_runnable(self, original_runnable):
        """Wrap a runnable with session history functionality.

        Args:
            original_runnable: The runnable instance to which session history will be added.

        Returns:
            An instance of RunnableWithMessageHistory that incorporates session history.
        """
        return RunnableWithMessageHistory(
            original_runnable,
            self.memory.get_session_history,  # Retrieve session history
            input_messages_key="customer_input",  # Key for user inputs
            history_messages_key="chat_history",  # Key for chat history
            history_factory_config=self.memory.get_history_factory_config(),  # Config for history factory
        ).with_config(
            {
                "run_name": original_runnable.__class__.__name__
            }  # Add runnable name for tracking
        )



    def get_user_intent(self, user_input: Dict):
        """Classify the user intent based on the input text.

        Args:
            user_input: The input text from the user.

        Returns:
            The classified intent of the user input.
        """
        # Retrieve possible routes for the user's input using the classifier
        intent_routes = self.intention_classifier.retrieve_multiple_routes(
            user_input["customer_input"]
        )

        # Handle cases where no intent is identified
        if len(intent_routes) == 0:
            return None
        else:
            intention = intent_routes[0].name  # Use the first matched intent

        # Validate the retrieved intention and handle unexpected types
        if intention is None:
            return None
        elif isinstance(intention, str):
            return intention
        else:
            # Log the intention type for unexpected cases
            intention_type = type(intention).__name__
            print(
                f"I'm sorry, I didn't understand that. The intention type is {intention_type}."
            )
            return None



#Functions to handle each intention

    def handle_know_mission(self, user_input: Dict[str, str]) -> str:

        response = self.rag(user_input,index_name = "pdf-data", config=self.memory_config)

        return response

    def handle_know_services(self, user_input: Dict[str, str]) -> str:

        response = self.rag.invoke(user_input,index_name = "pdf-data", config=self.memory_config)

        return response

        """
        Extracts dates from the input text.

        Args:
            text: The input text from the user.

        Returns:
            A dictionary with possible start_date and end_date.
        """
        words = text.split()
        dates = [parse(word, fuzzy=True) for word in words if self.is_date(word)]
        if len(dates) == 1:
            return {"start_date": dates[0].strftime('%Y-%m-%d'), "end_date": None}
        elif len(dates) >= 2:
            return {"start_date": dates[0].strftime('%Y-%m-%d'), "end_date": dates[1].strftime('%Y-%m-%d')}
        return {"start_date": None, "end_date": None}

    '''def handle_recall_entry(self, user_input: Dict):
        """Handle the intent to recall past journal entries based on theme or date.

        Args:
            user_input: The input text specifying the desired entries.

        Returns:
            A list or structured view of relevant entries.
        """
        # Extract dates from user input
        dates = self.extract_dates(user_input["customer_input"])

        # Retrieve the chain for recalling entries
        retrieve_chain = self.get_chain("chat_about_journal")[0]  # Assuming the first chain is for retrieval

        # Set the appropriate Pinecone index based on user input
        if "index_name" in user_input:
            retrieve_chain.set_pinecone_index(user_input["index_name"])

        # Determine if the user wants to search by date or theme
        if dates["start_date"] or dates["end_date"]:
            entries = retrieve_chain.get_entries_by_date(
                user_id=self.user_id,
                entry_type=user_input.get("entry_type", "journal"),
                start_date=dates["start_date"],
                end_date=dates["end_date"]
            )
        else:
            entries = retrieve_chain.query_relevant_entries(
                user_input=user_input["theme"]
            )

        # Format the entries for presentation
        present_chain = self.get_chain("chat_about_journal")[1]  # Assuming the second chain is for presentation
        response = present_chain.format_output(entries, user_input.get("entry_type", "journal"))

        return response
        '''
    
    def handle_habit_alternatives(self, user_input: Dict[str, str]) -> str:

        response = self.rag.invoke(user_input,index_name = "pdf-data", config=self.memory_config)

        return response       

    def handle_find_therapist(self, user_input: Dict):
        response = self.rag.invoke(user_input,index_name = "therapists", config=self.memory_config)

        return response 

    def handle_find_support_group(self, user_input: Dict):
        response = self.rag.invoke(user_input,index_name = "support-group", config=self.memory_config)

        return response 

    def handle_find_hotline(self, user_input: Dict):
        response = self.rag.invoke(user_input,index_name = "hotlines", config=self.memory_config)

        return response

    def extract_message(self, message: str) -> str:
        """Extract the message content from the user input message using the configured LLM."""
        prompt = f"Extract the message content from the following input: '{message}'. The user's message should contain the intention to add to a journal or mood board and the message content you should extract. Output only the extracted message"
        response = self.llm.invoke(prompt)
        
        # Extract the relevant part from the response content
        extracted_message = response.content.split('The message content to extract from the input is: "', 1)[-1].rsplit('"', 1)[0]
        print(f"Extracted message content: {extracted_message}")  # Debug print
        return extracted_message

    def handle_insert_journal(self, user_input: Dict[str, str]) -> str:
        """
        Handles journal entry intent by processing user input and providing a response.
        """
        message = user_input.get("customer_input", "")
        print(f"User message: {message}")  # Debug print
        extracted_message = self.extract_message(message)
    
        # Step 1: Process user message with the reasoning chain
        result = JournalEntryManager(self.db_manager).process(user_id=self.user_id, user_message=extracted_message)
    
        # Step 2: Generate response with the response chain
        response = JournalEntryResponse().generate(result)
    
        return response



    def handle_insert_mood(self, user_input: Dict):
        """Handle the intent to make an entry in the mood board.
    
        Args:
            user_input: The input text from the user.
    
        Returns:
            Confirmation message after successfully processing the mood board entry.
        """
        message = user_input.get("customer_input", "")
        print(f"User message: {message}")  # Debug print
        extracted_message = self.extract_message(message)
    
        # Step 1: Process user message with the reasoning chain
        result = MoodEntryManager(db_manager=self.db_manager).process(user_id=self.user_id, mood=extracted_message)
    
        # Step 2: Generate response with the response chain
        response = MoodEntryResponse().generate(result)
        return response
    
    def handle_view_journal(self, user_input: Dict):
        """Handle the intent to view past journal entries.
    
        Args:
            user_input: The input text specifying the desired journal entries.
    
        Returns:
            A list or structured view of relevant journal entries.
        """
        message = user_input.get("customer_input", "")
        journal_handler = JournalInteractionHandler(JournalQueryChain(), JournalResponseChain(llm=self.llm))
        response = journal_handler.handle_input(user_input = message, user_id = self.user_id)
    
        return response
    
    def handle_view_mood(self, user_input: Dict):
        """Handle the intent to view past mood board entries.
    
        Args:
            user_input: The input text specifying the desired mood board entries.
    
        Returns:
            A list or structured view of relevant mood board entries.
        """
        message = user_input.get("customer_input", "")
        mood_handler = MoodInteractionHandler(MoodQueryChain(), MoodResponseChain(llm=self.llm))
        response = mood_handler.handle_input(user_input = message, user_id = self.user_id)
    
        return response

    def handle_insert_gratitude(self, user_input: Dict):
        """Handle the intent to make an entry on the community gratitude banner.

        Args:
            user_input: The input text from the user expressing gratitude or positivity.

        Returns:
            Confirmation message after successfully posting to the gratitude banner.
        """
        # Retrieve the chain for creating a gratitude banner entry
        user_message = user_input.get("customer_input", "")
        # Step 1: Process user message with the reasoning chain
        result = GratitudeEntryManager(db_manager=self.db_manager).process( message=user_message)

        # Step 2: Generate response with the response chain
        response = GratitudeEntryResponse().generate(result)
        return response

    def handle_delete_journal(self, user_input: Dict):
        """Handle the intent to delete a journal entry.
    
        Args:
            user_input: The input text specifying the journal entry to delete.
    
        Returns:
            Confirmation message after successfully deleting the journal entry.
        """
        deleter_chain = JournalEntryDeleter(self.db_manager)
        confirmation_chain = DeletionConfirmationFormatter()
    
        # Extract the date from user input
        message = user_input.get("message", "")
        # print(f"User message: {message}")  # Debug print
        date = self.extract_date(message)
        if not date:
            return "Please provide the date of the journal entry you want to delete in the format YYYY-MM-DD."
    
        # Process the deletion
        deletion_result = deleter_chain.process(self.user_id, date)
    
        # Generate and return the confirmation message
        return confirmation_chain.format_output(deletion_result, date)
    
    def handle_delete_mood(self, user_input: Dict):
        """Handle the intent to delete data from the user's mood board.
    
        Args:
            user_input: The input text specifying the mood board entry to delete.
    
        Returns:
            Confirmation message after successfully deleting the mood board entry.
        """
        deleter_chain = MoodBoardEntryDeleter(self.db_manager)
        confirmation_chain = MoodBoardDeletionConfirmationFormatter()
    
        # Extract the date from user input
        message = user_input.get("message", "")
        # print(f"User message: {message}")  # Debug print
        date = self.extract_date(message)
        if not date:
            return "Please provide the date of the mood board entry you want to delete in the format YYYY-MM-DD."
    
        # Process the deletion
        deletion_result = deleter_chain.process(self.user_id, date)
    
        # Generate and return the confirmation message
        return confirmation_chain.format_output(deletion_result, date)
    
    def extract_date(self, message: str) -> str:
        """Extract date from the user input message."""
        # print(f"Extracting date from message: {message}")  # Debug print
        match = re.search(r'\d{4}-\d{2}-\d{2}', message)
        extracted_date = match.group(0) if match else None
        # print(f"Extracted date: {extracted_date}")  # Debug print
        return extracted_date

    def handle_update_journal(self, user_input: Dict):
        """Handle the intent to update a journal entry.
    
        Args:
            user_input: The input text specifying the journal entry to update.
    
        Returns:
            A confirmation message after successfully updating the journal entry.
        """
        user_id = self.user_id  # Assuming self.user_id is set to the current user's ID
        identifier_chain = IdentifyJournalEntryToModify()
        modifier_chain = ModifyJournalEntry(self.db_manager)
        confirmation_chain = InformUserOfJournalChange()
    
        # Extract the date and new content from user input
        message = user_input.get("message", "")
        # print(f"User message: {message}")  # Debug print
        date = self.extract_date(message)
        new_content = self.extract_new_content(message)
        # print(f"New content: {new_content}")  # Debug print
    
        if not date:
            return "Please provide the date of the journal entry you want to update in the format YYYY-MM-DD."
        if not new_content:
            return "Please provide the new content for the journal entry."
    
        # Retrieve the entry to modify
        entry = identifier_chain.get_entry_to_modify(user_id, date, self.db_manager)
        if not entry:
            return f"No journal entry found for the date {date}."
        # print(entry)  # Debug print

        # Modify the entry
        modification_result = modifier_chain.modify_entry(entry[0], new_content)
    
        # Generate and return the confirmation message
        return confirmation_chain.format_output(modification_result)
    
    def extract_new_content(self, message: str) -> str:
        """Extract new content from the user input message using the configured LLM."""
        prompt = f"Extract the new content from the following message: '{message}'. This is the content the user wants to update the entry with. The user's message should contain the intention to update, the date to update from, and the new content you should extract. Output only the extracted content"
        response = self.llm.invoke(prompt)
        
        # Extract the relevant part from the response content
        new_content = response.content.split('The new content to extract is: "', 1)[-1].rsplit('"', 1)[0]
        # print(f"Extracted new content: {new_content}")  # Debug print
        return new_content

    def handle_update_mood(self, user_input: Dict):
        """Handle the intent to update a mood board entry.
    
        Args:
            user_input: The input text specifying the mood board entry to update.
    
        Returns:
            A confirmation message after successfully updating the mood board entry.
        """
        identifier_chain = IdentifyMoodBoardEntryToModify()
        modifier_chain = ModifyMoodBoardEntry(self.db_manager)
        confirmation_chain = InformUserOfMoodBoardChange()
    
        # Extract the date and new content from user input
        message = user_input.get("message", "")
        # print(f"User message: {message}")  # Debug print
        date = self.extract_date(message)
        new_content = self.extract_new_content(message)
    
        if not date:
            return "Please provide the date of the mood board entry you want to update in the format YYYY-MM-DD."
        if not new_content:
            return "Please provide the new content for the mood board entry."
    
        # Retrieve the entry to modify
        entry = identifier_chain.get_entry_to_modify(self.user_id, date, self.db_manager)
        if not entry:
            return f"No mood board entry found for the date {date}."
    
        # Modify the entry
        modification_result = modifier_chain.modify_entry(entry["mood_id"], new_content)
    
        # Generate and return the confirmation message
        return confirmation_chain.format_output(modification_result)
    
    def handle_review_user_memory(self, user_input: Dict):
        """Handle the intent to review the user's stored data.
    
        Args:
            user_input: The input text specifying the time window for data retrieval.
    
        Returns:
            A formatted string presenting the user's stored data.
        """

        message = user_input.get("customer_input", "")
        mood_handler = UserInteractionHandler(UserQueryChain(), UserResponseChain(llm=self.llm))
        response = mood_handler.handle_input(user_input = message, user_id = self.user_id)
    
        return response
    
    def handle_chitchat_intent(self, user_input: Dict[str, str]) -> str:
        """Handle the chitchat intent by providing a response.

        Args:
            user_input: The input text from the user.

        Returns:
            The content of the response after processing through the chitchat chain.
        """

        response =self.chitchat_response_chain.invoke(user_input, config=self.memory_config)
        return response

    def handle_unknown_intent(self, user_input: Dict[str, str]) -> str:
        """Handle unknown intents by providing a chitchat response.

        Args:
            user_input: The input text from the user.

        Returns:
            The content of the response after processing through the new chain.
        """
        possible_intention = ["review_user_memory",
                                "find_therapist",
                                "find_support_group",
                                "find_hotline",
                                "habit_alternatives",
                                "insert_mood",
                                "delete_mood",
                                "update_mood",
                                "view_mood",
                                "insert_journal",
                                "delete_journal",
                                "view_journal",
                                "insert_gratitude",
                                "ask_missionvalues",
                                "ask_features",
                                "review_user_memory"
                                ]


        input_message = {}

        input_message["customer_input"] = user_input["customer_input"]
        input_message["possible_intentions"] = possible_intention
        input_message["chat_history"] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        )


      
        print("Chitchat")
        return self.handle_chitchat_intent(user_input)


    def save_memory(self) -> None:
        """Save the current memory state of the bot."""
        self.memory.save_session_history(self.user_id, self.conversation_id)

    def process_user_input(self, user_input: Dict[str, str]) -> str:
        """Process user input by routing through the appropriate intention pipeline.
    
        Args:
            user_input: The input text from the user.
    
        Returns:
            The content of the response after processing through the chains.
        """
        # Classify the user's intent based on their input
        intention = self.get_user_intent(user_input)
    
        print("Intent:", intention)
    
        # Route the input based on the identified intention
        handler = self.intent_handlers.get(intention, self.handle_unknown_intent)
    
        # Ensure the user input message is passed correctly
        user_input["message"] = user_input.get("customer_input", "")
    
        return handler(user_input)