# Import necessary classes and modules for chatbot functionality
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

from chatbot.chains.chitchat import ChitChatClassifierChain, ChitChatResponseChain
from chatbot.chains.chat_about_journal import RetrieveRelevantEntries, GenerateEmpatheticResponse
from chatbot.chains.delete_journal import JournalEntryDeleter, DeletionConfirmationFormatter
from chatbot.chains.delete_mood import MoodBoardEntryDeleter, MoodBoardDeletionConfirmationFormatter
from chatbot.chains.find_hotline import IdentifyHotlinePreferences, HotlineFinder, HotlineOutputFormatter
from chatbot.chains.find_support_group import IdentifySupportGroupPreferences, SupportGroupFinder, SupportGroupOutputFormatter
from chatbot.chains.find_therapist import IdentifyUserPreferences, TherapistFinder, TherapistOutputFormatter
from chatbot.chains.insert_gratitude import GratitudeManager
from chatbot.chains.insert_journal import JournalManager, JournalEntryResponse
from chatbot.chains.insert_mood import RetrieveEntries, PresentEntries
from chatbot.chains.review_user_memory import RetrieveUserData, PresentUserData
from chatbot.chains.update_journal import IdentifyJournalEntryToModify, ModifyJournalEntry, InformUserOfJournalChange
from chatbot.chains.update_mood import IdentifyMoodBoardEntryToModify, ModifyMoodBoardEntry, InformUserOfMoodBoardChange


class MainChatbot:
    """A bot that handles customer service interactions by processing user inputs and
    routing them through configured reasoning and response chains.
    """

    def __init__(self):
        """Initialize the bot with session and language model configurations."""
        # Initialize the memory manager to manage session history
        self.memory = MemoryManager()

        # Configure the language model with specific parameters for response generation
        self.llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini")

        # Map intent names to their corresponding reasoning and response chains
        self.chain_map = {

    
                "chat_about_journal": {
                    "retrieve": RetrieveRelevantEntries(pinecone_index="your_pinecone_index", embedding_model="your_embedding_model"),
                    "generate": GenerateEmpatheticResponse(prompt_template="Your template here")
                },
                "delete_mood": {
                    "delete": MoodBoardEntryDeleter(db_manager=DatabaseManager()),
                    "confirm": MoodBoardDeletionConfirmationFormatter()
                },
                "delete_journal": {
                    "delete": JournalEntryDeleter(db_manager=DatabaseManager()),
                    "confirm": DeletionConfirmationFormatter()
                },
                "find_hotline": {
                    "identify": IdentifyHotlinePreferences(),
                    "find": HotlineFinder(db_manager=DatabaseManager()),
                    "output": HotlineOutputFormatter()
                },
                "find_therapist": {
                    "identify": IdentifyUserPreferences(),
                    "find": TherapistFinder(db_manager=DatabaseManager()),
                    "output": TherapistOutputFormatter()
                },
                "find_support_group": {
                    "identify": IdentifySupportGroupPreferences(),
                    "find": SupportGroupFinder(db_manager=DatabaseManager()),
                    "output": SupportGroupOutputFormatter()
                },
                    "insert_mood": {
                    "retrieve": RetrieveEntries(db_manager=DatabaseManager()),
                    "present": PresentEntries()
                },
                "insert_journal": {
                    "insert": JournalManager(db_manager=DatabaseManager()),
                    "response": JournalEntryResponse()
                },
                "insert_gratitude": {
                    "insert": GratitudeManager(db_manager=DatabaseManager()),
                    "response": GratitudeManager(db_manager=DatabaseManager())
                },
                "review_user_memory": {
                    "retrieve": RetrieveUserData(db_manager=DatabaseManager()),
                    "present": PresentUserData(prompt_template="Your template here")
                },
                "update_mood": {
                    "identify": IdentifyMoodBoardEntryToModify(),
                    "modify": ModifyMoodBoardEntry(db_manager=DatabaseManager()),
                    "inform": InformUserOfMoodBoardChange()
                },
                "update_journal": {
                    "identify": IdentifyJournalEntryToModify(),
                    "modify": ModifyJournalEntry(db_manager=DatabaseManager()),
                    "inform": InformUserOfJournalChange()
                },
                "chitchat": {
                "reasoning": ChitChatClassifierChain(llm=self.llm),
                "response": self.add_memory_to_runnable(
                    ChitChatResponseChain(llm=self.llm)
                )
            }}



        self.rag = self.add_memory_to_runnable(
            RAGPipeline(
                index_name="rag",
                embeddings_model="text-embedding-3-small",
                llm=self.llm,
                memory=True,
            ).rag_chain
        )

        # Map of intentions to their corresponding handlers
        self.intent_handlers: Dict[Optional[str], Callable[[Dict[str, str]], str]] = {
        "review_user_memory": self.handle_support_information,
        "find_therapist": self.handle_find_therapist,
        "find_support_group": self.handle_find_support_group,
        "find_hotline": self.handle_find_hotline,
        "habit_alternatives": self.handle_habit_alternatives,
        "insert_mood": self.handle_insert_mood,
        "insert_journal": self.handle_insert_journal,
        "insert_gratitude": self.handle_insert_gratitude,
        "ask_missionvalues": self.handle_know_mission,
        "ask_features": self.handle_know_services,
        "review_user_memory": self.handle_know_data,
        "update_journal": self.handle_update_journal,
        "update_mood": self.handle_update_mood,
        "chat_about_journal": self.handle_recall_entry,
        "delete_journal":self.handle_delete_journal,
        "delete_mood":self.handle_delete_mood,
        "chat_about_journal": self.handle_recall_entry
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

        response = self.rag.invoke(user_input,index_name = "pdf-data", config=self.memory_config)

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

    def handle_recall_entry(self, user_input: Dict):
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

    def handle_insert_journal(self, user_input: Dict):
        """Handle the intent to make an entry in the journal.

        Args:
            user_input: The input text from the user.

        Returns:
            Confirmation message after successfully processing the journal entry.
        """
        # Retrieve the chain for journal entry creation
        entry_chain = self.get_chain("insert_journal")

        # Process the user input through the entry chain
        response = entry_chain.invoke(user_input)

        return response.content

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
        # Retrieve the chain for viewing journal entries
        view_chain = self.get_chain("view_journal")

        # Query the chain for the requested journal entries
        response = view_chain.invoke(user_input)

        return response.content
    
    def handle_view_mood(self, user_input: Dict):
        """Handle the intent to view past mood board entries.

        Args:
            user_input: The input text specifying the desired mood board entries.

        Returns:
            A list or structured view of relevant mood board entries.
        """
        # Retrieve the chain for viewing mood board entries
        view_chain = self.get_chain("view_mood")

        # Query the chain for the requested mood board entries
        response = view_chain.invoke(user_input)

        return response.content


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
        """Handle the intent to delete data from the user's journal.

        Args:
            user_input: The input text specifying the journal entry to delete.

        Returns:
            Confirmation message after successfully deleting the journal entry.
        """
        # Retrieve the chain for deleting a journal entry
        delete_chain = self.get_chain("delete_journal")

        # Process the user input through the delete chain
        response = delete_chain.invoke(user_input)

        return response.content

    def handle_delete_mood(self, user_input: Dict):
        """Handle the intent to delete data from the user's mood board.

        Args:
            user_input: The input text specifying the mood board entry to delete.

        Returns:
            Confirmation message after successfully deleting the mood board entry.
        """
        # Retrieve the chain for deleting a mood board entry
        delete_chain = self.get_chain("delete_mood")

        # Process the user input through the delete chain
        response = delete_chain.invoke(user_input)

        return response.content

    def handle_update_journal(self, user_input: Dict):
        """Handle the intent to alter data in the user's journal.

        Args:
            user_input: The input text specifying the journal entry to alter and new data.

        Returns:
            Confirmation message after successfully updating the journal entry.
        """
        # Retrieve the chain for altering a journal entry
        alter_chain = self.get_chain("update_journal")

        # Process the user input through the alter chain
        response = alter_chain.invoke(user_input)

        return response.content

    def handle_update_mood(self, user_input: Dict):
        """Handle the intent to alter data in the user's mood board.

        Args:
            user_input: The input text specifying the mood board entry to alter and new data.

        Returns:
            Confirmation message after successfully updating the mood board entry.
        """
        # Retrieve the chain for altering a mood board entry
        alter_chain = self.get_chain("update_mood")

        # Process the user input through the alter chain
        response = alter_chain.invoke(user_input)

        return response.content


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
        return handler(user_input)
