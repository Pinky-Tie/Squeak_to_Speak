# Import necessary classes and modules for chatbot functionality
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from typing import Callable, Dict, Optional, List, Union
from dateutil.parser import parse

from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from chatbot.memory import MemoryManager
from chatbot.router.loader import load_intention_classifier

from chatbot.memory import MemoryManager
from chatbot.router.loader import load_intention_classifier
from data.database_functions import DatabaseManager
from chatbot.rag import RAGPipeline

#Maria
"""
from .chains.chitchat import ChitChatClassifierChain, ChitChatResponseChain
from .chains.chat_about_journal import RetrieveRelevantEntries, GenerateEmpatheticResponse
from .chains.delete_journal import JournalEntryDeleter, DeletionConfirmationFormatter
from .chains.delete_mood import MoodBoardEntryDeleter, MoodBoardDeletionConfirmationFormatter
from .chains.find_hotline import IdentifyHotlinePreferences, HotlineFinder, HotlineOutputFormatter
from .chains.find_support_group import IdentifySupportGroupPreferences, SupportGroupFinder, SupportGroupOutputFormatter
from .chains.find_therapist import IdentifyUserPreferences, TherapistFinder, TherapistOutputFormatter
from .chains.insert_gratitude import GratitudeManager
from .chains.insert_journal import JournalManager, JournalEntryResponse
from .chains.insert_mood import RetrieveEntries, PresentEntries
from .chains.review_user_memory import RetrieveUserData, PresentUserData
from .chains.update_journal import IdentifyJournalEntryToModify, ModifyJournalEntry, InformUserOfJournalChange
from .chains.update_mood import IdentifyMoodBoardEntryToModify, ModifyMoodBoardEntry, InformUserOfMoodBoardChange
import sqlite3
db_file = r'C:\Users\maria\OneDrive - NOVAIMS\Documents\Uni related\3º Ano\Capstone Project\Squeak_to_Speak\Squeak_to_speak\data\database\squeaktospeak_db.db'
# Connect to the SQLite database
conn = sqlite3.connect(db_file)
db_manager = DatabaseManager(conn)
"""

from chatbot.chains.chitchat import ChitChatClassifierChain, ChitChatResponseChain
from chatbot.chains.chat_about_journal import RetrieveRelevantEntries, GenerateEmpatheticResponse
from chatbot.chains.delete_journal import JournalEntryDeleter, DeletionConfirmationFormatter
from chatbot.chains.delete_mood import MoodBoardEntryDeleter, MoodBoardDeletionConfirmationFormatter
from chatbot.chains.find_hotline import IdentifyHotlinePreferences, HotlineFinder, HotlineOutputFormatter
from chatbot.chains.find_support_group import IdentifySupportGroupPreferences, SupportGroupFinder, SupportGroupOutputFormatter
from chatbot.chains.find_therapist import IdentifyUserPreferences, TherapistFinder, TherapistOutputFormatter
from chatbot.chains.insert_gratitude import GratitudeEntryManager
from chatbot.chains.insert_journal import JournalEntryManager, JournalEntryResponse
from chatbot.chains.insert_mood import MoodEntryManager, MoodEntryResponse
from chatbot.chains.review_user_memory import RetrieveUserData, PresentUserData
from chatbot.chains.update_journal import IdentifyJournalEntryToModify, ModifyJournalEntry, InformUserOfJournalChange
from chatbot.chains.update_mood import IdentifyMoodBoardEntryToModify, ModifyMoodBoardEntry, InformUserOfMoodBoardChange
from chatbot.chains.view_journal import RetrieveJournalEntries, PresentJournalEntries
from chatbot.chains.view_mood import RetrieveMoodBoardEntries, PresentMoodBoardEntries


#databse connection
import sqlite3
db_file = r'D:\MARGARIDA\dificuldade\3rd_year\capstone_project\Squeak_to_Speak\Squeak_to_speak\data\database\squeaktospeak_db.db'

conn = sqlite3.connect(db_file)
db_manager = DatabaseManager(conn)


class MainChatbot:
    """A bot that handles customer service interactions by processing user inputs and
    routing them through configured reasoning and response chains.
    """

    def _init_(self, user_id: int, conversation_id: int):
        """Initialize the bot with session and language model configurations."""
        # Initialize the memory manager to manage session history
        self.memory = MemoryManager()

        # Configure the language model with specific parameters for response generation
        self.llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini")

        self.db_manager = DatabaseManager(conn)
        self.journal_manager = JournalEntryManager(self.db_manager)
        self.journal_response = JournalEntryResponse()
        self.user_id = user_id
        self.conversation_id = conversation_id
        self.memory_config = {
            "configurable": {
                "user_id": self.user_id,
                "conversation_id": self.conversation_id,
            }
        }

        # Initialize handlers for each intent
        self.mood_board_entry_deleter = MoodBoardEntryDeleter(db_manager=self.db_manager)
        self.mood_board_deletion_confirmation_formatter = MoodBoardDeletionConfirmationFormatter()
        self.journal_entry_deleter = JournalEntryDeleter(db_manager=self.db_manager)
        self.deletion_confirmation_formatter = DeletionConfirmationFormatter()
        self.identify_hotline_preferences = IdentifyHotlinePreferences()
        self.hotline_finder = HotlineFinder(db_manager=self.db_manager)
        self.hotline_output_formatter = HotlineOutputFormatter()
        self.identify_user_preferences = IdentifyUserPreferences()
        self.therapist_finder = TherapistFinder(db_manager=self.db_manager)
        self.therapist_output_formatter = TherapistOutputFormatter()
        self.identify_support_group_preferences = IdentifySupportGroupPreferences()
        self.support_group_finder = SupportGroupFinder(db_manager=self.db_manager)
        self.support_group_output_formatter = SupportGroupOutputFormatter()
        self.retrieve_journal_entries = RetrieveJournalEntries(db_manager=self.db_manager, rag_pipeline=self.rag)
        self.present_journal_entries = PresentJournalEntries()
        self.journal_manager = JournalEntryManager(db_manager=self.db_manager)
        self.journal_entry_response = JournalEntryResponse()
        self.gratitude_manager = GratitudeEntryManager(db_manager=self.db_manager)
        self.retrieve_user_data = RetrieveUserData(db_manager=self.db_manager)
        self.present_user_data = PresentUserData()
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
            "find_hotline": {
                "identify": self.identify_hotline_preferences,
                "find": self.hotline_finder,
                "output": self.hotline_output_formatter
            },
            "find_therapist": {
                "identify": self.identify_user_preferences,
                "find": self.therapist_finder,
                "output": self.therapist_output_formatter
            },
            "find_support_group": {
                "identify": self.identify_support_group_preferences,
                "find": self.support_group_finder,
                "output": self.support_group_output_formatter
            },
            "insert_mood": {
                "retrieve": self.retrieve_journal_entries,
                "present": self.present_journal_entries
            },
            "insert_journal": {
                "insert": self.journal_manager,
                "response": self.journal_entry_response
            },
            "insert_gratitude": {
                "insert": self.gratitude_manager,
                "response": self.gratitude_manager
            },
            "review_user_memory": {
                "retrieve": self.retrieve_user_data,
                "present": self.present_user_data
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


        self.rag = self.add_memory_to_runnable(
            RAGPipeline(
                index_name="pdf-data",
                embeddings_model="text-embedding-3-small",
                llm=self.llm,
                memory=True,
            ).rag_chain
        )

        # Map of intentions to their corresponding handlers
        self.intent_handlers: Dict[Optional[str], Callable[[Dict[str, str]], str]] = {
        #"review_user_memory": self.handle_support_information,
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
        #"chat_about_journal": self.handle_recall_entry,
        "delete_journal":self.handle_delete_journal,
        "delete_mood":self.handle_delete_mood,
        'chitchat':self.handle_chitchat_intent
        }
        # Load the intention classifier to determine user intents
        self.intention_classifier = load_intention_classifier()

    def user_login(self, user_id: str, conversation_id: str) -> None:
        """Log in a user by setting the user and conversation identifiers.

        Args:
            user_id: Identifier for the user.
            conversation_id: Identifier for the conversation.
        """
        self.user_id = user_id
        self.conversation_id = conversation_id
        self.memory_config = {
            "configurable": {
                "user_id": self.user_id,
                "conversation_id": self.conversation_id,
            }
        }

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

    def get_chain(self, intent: str):
        """Retrieve the reasoning and response chains based on user intent.

        Args:
            intent: The identified intent of the user input.

        Returns:
            A tuple containing the reasoning and response chain instances for the intent.
        """
        return self.chain_map[intent]["reasoning"], self.chain_map[intent]["response"]

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

    def get_random_gratitude_message(self) -> str:
        """
        Retrieves a random gratitude message from the gratitude_entries table.

        Returns:
            A random gratitude message.
        """
        query = """
        SELECT content
        FROM gratitude_entries
        ORDER BY RANDOM()
        LIMIT 1
        """
        result = self.db_manager.select(query)
        if result:
            return result[0]['content']
        else:
            return "No gratitude messages found."

#Functions to handle each intention

    def handle_know_mission(self, user_input: Dict[str, str]) -> str:

        response = self.rag.ma(user_input,index_name = "pdf-data", config=self.memory_config)

        return response

    def handle_know_services(self, user_input: Dict[str, str]) -> str:

        response = self.rag.invoke(user_input,index_name = "pdf-data", config=self.memory_config)

        return response

    def extract_dates(self, text: str) -> Dict[str, Union[str, None]]:
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

    def is_date(self, string: str) -> bool:
        """
        Checks if a string can be parsed as a date.

        Args:
            string: The input string.

        Returns:
            True if the string can be parsed as a date, False otherwise.
        """
        try:
            parse(string, fuzzy=False)
            return True
        except ValueError:
            return False

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

        return response'''

    def handle_habit_alternatives(self, user_input: Dict[str, str]) -> str:

        response = self.rag.invoke(user_input,index_name = "pdf-data", config=self.memory_config)

        return response       

    def handle_find_therapist(self, user_input: Dict):
        """Handle the healthcare professional recommendation intent.

        Args:
            user_input: The input text from the user.

        Returns:
            The content of the response after processing through the chains.
        """
        # Retrieve reasoning and response chains for the healthcare recommendation intent
        reasoning_chain, response_chain = self.get_chain("find_therapist")

        # Process user input through the reasoning chain
        reasoning_output = reasoning_chain.invoke(user_input)

        # Generate a response using the output of the reasoning chain
        response = response_chain.invoke(reasoning_output, config=self.memory_config)

        return response.content

    def handle_find_support_group(self, user_input: Dict):
        """Handle the support group recommendation intent.

        Args:
            user_input: The input text from the user.

        Returns:
            The content of the response after processing through the chains.
        """
        # Retrieve reasoning and response chains for the support group recommendation intent
        reasoning_chain, response_chain = self.get_chain("find_support_group")

        # Process user input through the reasoning chain
        reasoning_output = reasoning_chain.invoke(user_input)

        # Generate a response using the output of the reasoning chain
        response = response_chain.invoke(reasoning_output, config=self.memory_config)

        return response.content

    def handle_find_hotline(self, user_input: Dict):
        """Handle the emergency or non-emergency hotline contact intent.

        Args:
            user_input: The input text from the user.

        Returns:
            The content of the response after processing through the chains.
        """
        # Retrieve reasoning and response chains for the hotline contact intent
        reasoning_chain, response_chain = self.get_chain("find_hotline")

        # Process user input through the reasoning chain
        reasoning_output = reasoning_chain.invoke(user_input)

        # Generate a response using the output of the reasoning chain
        response = response_chain.invoke(reasoning_output, config=self.memory_config)

        return response.content

    def handle_insert_journal(self, user_input: Dict[str, str]) -> str:
        """
        Handles journal entry intent by processing user input and providing a response."""
        user_message = user_input.get("message", "")
        # Step 1: Process user message with the reasoning chain
        result = self.journal_manager.process(user_id=self.user_id, user_message=user_message)

        # Step 2: Generate response with the response chain
        response = self.journal_response.generate(result["success"])

        return response

    def handle_insert_mood(self, user_input: Dict):
        """Handle the intent to make an entry in the mood board.

        Args:
            user_input: The input text from the user.

        Returns:
            Confirmation message after successfully processing the mood board entry.
        """
        # Retrieve the chain for mood board entry creation
        entry_chain = self.get_chain("insert_mood")

        # Process the user input through the entry chain
        response = entry_chain.invoke(user_input)

        return response.content

    def handle_view_journal(self, user_input: Dict):
        """Handle the intent to view past journal entries.
    
        Args:
            user_input: The input text specifying the desired journal entries.
    
        Returns:
            A list or structured view of relevant journal entries.
        """
        retrieve_chain = self.get_chain("view_journal")[0] 
        present_chain = self.get_chain("view_journal")[1]

        if "search_type" not in user_input:
            # Prompt the user to choose between searching by date or topic
            return retrieve_chain.prompt_for_search_type()
        elif user_input["search_type"] == "date" and "date" not in user_input:
            # Prompt the user for the date if not provided
            return retrieve_chain.prompt_for_date()
        elif user_input["search_type"] == "topic" and "topic" not in user_input:
            # Prompt the user for the topic if not provided
            return retrieve_chain.prompt_for_topic()
        elif user_input["search_type"] == "date":
            # Retrieve the journal entries for the specified date
            entries = retrieve_chain.get_entries_by_date(self.user_id, user_input["date"])
        elif user_input["search_type"] == "topic":
            # Retrieve the journal entries for the specified topic
            entries = retrieve_chain.get_entries_by_topic(self.user_id, user_input["topic"])
        
        # Format the entries for presentation
        response = present_chain.format_output(entries)
        return response
    
    def handle_view_mood(self, user_input: Dict):
        """Handle the intent to view past mood board entries.
    
        Args:
            user_input: The input text specifying the desired mood board entries.
    
        Returns:
            A list or structured view of relevant mood board entries.
        """
        retrieve_chain = self.get_chain("view_mood")[0]
        present_chain = self.get_chain("view_mood")[1]
    
        if "search_type" not in user_input:
            # Prompt the user to choose between searching by date or topic
            return retrieve_chain.prompt_for_search_type()
        elif user_input["search_type"] == "date" and "date" not in user_input:
            # Prompt the user for the date if not provided
            return retrieve_chain.prompt_for_date()
        elif user_input["search_type"] == "topic" and "topic" not in user_input:
            # Prompt the user for the topic if not provided
            return retrieve_chain.prompt_for_topic()
        elif user_input["search_type"] == "date":
            # Retrieve the mood board entries for the specified date
            entries = retrieve_chain.get_entries_by_date(self.user_id, user_input["date"])
        elif user_input["search_type"] == "topic":
            # Retrieve the mood board entries for the specified topic
            entries = retrieve_chain.get_entries_by_topic(self.user_id, user_input["topic"])
        
        # Format the entries for presentation
        response = present_chain.format_output(entries)
        return response

    def handle_insert_gratitude(self, user_input: Dict):
        """Handle the intent to make an entry on the community gratitude banner.

        Args:
            user_input: The input text from the user expressing gratitude or positivity.

        Returns:
            Confirmation message after successfully posting to the gratitude banner.
        """
        # Retrieve the chain for creating a gratitude banner entry
        entry_chain = self.get_chain("insert_gratitude")

        # Process the user input through the entry chain
        response = entry_chain.invoke(user_input)

        return response.content

    def handle_delete_journal(self, user_input: Dict):
        """
        Handle the intent to delete data from the user's journal.

        Args:
            user_input: The input text specifying the journal entry to delete.

        Returns:
            Confirmation message after successfully deleting the journal entry.
        """
        delete_chain = self.get_chain("delete_journal")[0]

        if "date" not in user_input:
            # Prompt the user for the date if not provided
            return delete_chain.prompt_for_date()
        else:
            # Process the user input through the delete chain
            response = delete_chain.process(self.user_id, user_input["date"])
            confirmation_formatter = self.get_chain("delete_journal")[1]  # Assuming the second chain is for confirmation
            return confirmation_formatter.format_output(response, user_input["date"])

    def handle_delete_mood(self, user_input: Dict):
        """
        Handle the intent to delete data from the user's mood board.
    
        Args:
            user_input: The input text specifying the mood board entry to delete.
    
        Returns:
            Confirmation message after successfully deleting the mood board entry.
        """
        delete_chain = self.get_chain("delete_mood")[0]
    
        if "date" not in user_input:
            # Prompt the user for the date if not provided
            return delete_chain.prompt_for_date()
        else:
            # Process the user input through the delete chain
            response = delete_chain.process(self.user_id, user_input["date"])
            confirmation_formatter = self.get_chain("delete_mood")[1]
            return confirmation_formatter.format_output(response, user_input["date"])

    def handle_update_journal(self, user_input: Dict):
        """Handle the intent to alter data in the user's journal.
    
        Args:
            user_input: The input text specifying the journal entry to alter and new data.
    
        Returns:
            Confirmation message after successfully updating the journal entry.
        """
        identify_chain = self.get_chain("update_journal")[0]
        modify_chain = self.get_chain("update_journal")[1] 
        if "date" not in user_input:
            # Prompt the user for the date if not provided
            return identify_chain.prompt_for_date()
        elif "new_content" not in user_input:
            # Retrieve the entry to modify
            entry = identify_chain.get_entry_to_modify(self.user_id, user_input["date"], self.db_manager)
            if entry:
                # Store the entry ID in the user input for the next step
                user_input["entry_id"] = entry["entry_id"]
                # Prompt the user for the new content
                return modify_chain.prompt_for_new_content()
            else:
                return f"No journal entry found for date {user_input['date']}."
        else:
            # Process the user input through the modify chain
            response = modify_chain.modify_entry(user_input["entry_id"], user_input["new_content"])
            confirmation_formatter = self.get_chain("update_journal")[2]  # Assuming the third chain is for confirmation
            return confirmation_formatter.format_output(response)

    def handle_update_mood(self, user_input: Dict):
        """Handle the intent to alter data in the user's mood board.
    
        Args:
            user_input: The input text specifying the mood board entry to alter and new data.
    
        Returns:
            Confirmation message after successfully updating the mood board entry.
        """
        identify_chain = self.get_chain("update_mood")[0]
        modify_chain = self.get_chain("update_mood")[1] 
    
        if "date" not in user_input:
            # Prompt the user for the date if not provided
            return identify_chain.prompt_for_date()
        elif "new_content" not in user_input:
            # Retrieve the entry to modify
            entry = identify_chain.get_entry_to_modify(self.user_id, user_input["date"], self.db_manager)
            if entry:
                # Store the entry ID in the user input for the next step
                user_input["entry_id"] = entry["entry_id"]
                # Prompt the user for the new content
                return modify_chain.prompt_for_new_content()
            else:
                return f"No mood board entry found for date {user_input['date']}."
        else:
            # Process the user input through the modify chain
            response = modify_chain.modify_entry(user_input["entry_id"], user_input["new_content"])
            confirmation_formatter = self.get_chain("update_mood")[2]
            return confirmation_formatter.format_output(response)
    
    def handle_review_user_memory(self, user_input: Dict):
        """Handle the intent to review all data related to the user.
    
        Args:
            user_input: The input text specifying the request to review user data.
    
        Returns:
            A structured view of all relevant user data.
        """
        retrieve_chain = self.get_chain("review_user_memory")[0]  # Assuming the first chain is for retrieval
        present_chain = self.get_chain("review_user_memory")[1]  # Assuming the second chain is for presentation
    
        # Retrieve all relevant data for the user
        data = retrieve_chain.retrieve_data(self.user_id)
    
        # Format the data for presentation
        response = present_chain.format_output(data)
        return response
    
    def handle_chitchat_intent(self, user_input: Dict[str, str]) -> str:
        """Handle the chitchat intent by providing a response.

        Args:
            user_input: The input text from the user.

        Returns:
            The content of the response after processing through the chitchat chain.
        """
        _, chitchat_response_chain = self.get_chain("chitchat")

        response = chitchat_response_chain.invoke(user_input, config=self.memory_config)
        return response

    def handle_unknown_intent(self, user_input: Dict[str, str]) -> str:
        """Handle unknown intents by providing a chitchat response.

        Args:
            user_input: The input text from the user.

        Returns:
            The content of the response after processing through the new chain.
        """
        possible_intention = [
        "review_user_memory"
        "find_therapist"
        "find_support_group"
        "find_hotline"
        "habit_alternatives"
        "insert_mood"
        "insert_journal"
        "ask_missionvalues"
        "ask_features"
        "review_user_memory"
        "update_journal"
        "chat_about_journal"
        ]

        chitchat_reasoning_chain, _ = self.get_chain("chitchat")

        input_message = {}

        input_message["customer_input"] = user_input["customer_input"]
        input_message["possible_intentions"] = possible_intention
        input_message["chat_history"] = self.memory.get_session_history(
            self.user_id, self.conversation_id
        )

        reasoning_output1 = chitchat_reasoning_chain.invoke(input_message)

        if reasoning_output1.chitchat:
            print("Chitchat")
            return self.handle_chitchat_intent(user_input)
        else:
            router_reasoning_chain2, _ = self.get_chain("router")
            reasoning_output2 = router_reasoning_chain2.invoke(input_message)
            new_intention = reasoning_output2.intent
            print("New Intention:", new_intention)
            new_handler = self.intent_handlers.get(new_intention)
            return new_handler(user_input)

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
        
        # Check if the handler is for viewing, deleting, or updating a journal/mood entry and handle multi-step interaction
        if intention in ["view_journal", "view_mood", "delete_journal", "delete_mood", "update_journal", "update_mood"]:
            if "search_type" not in user_input and intention in ["view_journal", "view_mood"]:
                # Prompt for the search type if not provided
                return handler(user_input)
            elif "date" not in user_input and "topic" not in user_input:
                # Prompt for the date or topic if not provided
                return handler(user_input)
            elif "date" in user_input and "new_content" not in user_input and intention in ["update_journal", "update_mood"]:
                # Process the next step for updating a journal/mood entry
                return handler({"customer_input": user_input["customer_input"], "date": user_input["date"]})
            elif "topic" in user_input and "new_content" not in user_input and intention in ["update_journal", "update_mood"]:
                # Process the next step for updating a journal/mood entry
                return handler({"customer_input": user_input["customer_input"], "topic": user_input["topic"]})
            elif "date" in user_input and "new_content" in user_input and intention in ["update_journal", "update_mood"]:
                # Process the final step for updating a journal/mood entry
                return handler({"customer_input": user_input["customer_input"], "date": user_input["date"], "new_content": user_input["new_content"]})
            elif "date" in user_input and intention in ["view_journal", "view_mood"]:
                # Process the final step for viewing a journal/mood entry by date
                return handler({"customer_input": user_input["customer_input"], "date": user_input["date"]})
            elif "topic" in user_input and intention in ["view_journal", "view_mood"]:
                # Process the final step for viewing a journal/mood entry by topic
                return handler({"customer_input": user_input["customer_input"], "topic": user_input["topic"]})
        
        return handler(user_input)