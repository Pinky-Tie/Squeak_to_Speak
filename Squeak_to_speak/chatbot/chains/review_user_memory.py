# User Story: I want to review the data Squeak to Speak holds about me to better understand what is collected and how it is used.

# Chain 1
# Goal: Retrieve information on the user
# Implementation: This chain takes the user’s input, defines a time window for retrieval of the data and queries the database for all relevant entries inside that time window. It will then structure the information and output it.
from langchain.schema.runnable.base import Runnable
from pydantic import BaseModel, Field
# Define the product database as a dictionary with product categories
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from data.data_func import connect_database
from chatbot.chains.base import PromptTemplate, generate_prompt_templates



class UserInfo(BaseModel):
    """Model for representing user information."""
    username: str = Field(..., description="User's username")
    country: str = Field(..., description="User's country")
    user_id: int = Field(..., description="User ID")

class JournalInfo(BaseModel):
    """Model for representing Journal summary information."""
    entry_count: int = Field(..., description="Number of journal entries")
    first_entry_date: str = Field(..., description="Date of the first journal entry")

class MoodInfo(BaseModel):
    """Model for representing Mood Tracker summary information."""
    entry_count: int = Field(..., description="Number of mood entries")
    first_entry_date: str = Field(..., description="Date of the first mood entry")

class UserSummary(BaseModel):
    """Model for the result containing user data summary."""
    user_info: UserInfo
    journal_info: JournalInfo
    mood_info: MoodInfo

class UserQueryChain(Runnable):
    """Chain for querying user data from the database."""

    def get_user_info(self, user_id):
        conn, cursor = connect_database()
        try:
            query = "SELECT username, country, user_id FROM Users WHERE user_id = ?;"
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
        finally:
            conn.close()


        return UserInfo(username=row[0], country=row[1], user_id=row[2])

    def get_journal_info(self, user_id):
        conn, cursor = connect_database()
        try:
            query = """
            SELECT COUNT(*), MIN(date) 
            FROM Journal 
            WHERE user_id = ?;
            """
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
        finally:
            conn.close()

        return JournalInfo(entry_count=row[0], first_entry_date=row[1] or "No entries")

    def get_mood_info(self, user_id):
        conn, cursor = connect_database()
        try:
            query = """
            SELECT COUNT(*), MIN(date) 
            FROM Mood_tracker 
            WHERE user_id = ?;
            """
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
        finally:
            conn.close()

        return MoodInfo(entry_count=row[0], first_entry_date=row[1] or "No entries")

    def invoke(self, inputs):
        """Invoke the chain to fetch user summary information."""
        user_id = inputs.get("user_id")

        user_info = self.get_user_info(user_id)
        journal_info = self.get_journal_info(user_id)
        mood_info = self.get_mood_info(user_id)

        return UserSummary(user_info=user_info, journal_info=journal_info, mood_info=mood_info)

class UserResponseChain(Runnable):
    """Chain that generates a response summarizing user data."""

    def __init__(self, llm, memory=True):
        """Initialize the user response chain."""
        super().__init__()
        self.llm = llm

        prompt_template = PromptTemplate(
            system_template="""
            You are an assistant capable of retrieving and summarizing user information.
            Provide the following details in a clear and organized manner:

            1. Username and country.
            2. Number of journal entries and the date of the first entry.
            3. Number of mood tracker entries and the date of the first entry.

            Retrieved User Data:
            {user_data}
            """,
            human_template="""
            User Query:
            {user_query}
            """,
        )

        self.prompt = generate_prompt_templates(prompt_template, memory=memory)
        self.chain = self.prompt | self.llm

    def invoke(self, inputs, config):
        """Invoke the user response chain."""
        user_data = inputs.get("user_data")
        user_query = inputs.get("user_query")

        prompt_inputs = {
            "user_data": json.dumps(user_data.dict(), indent=4),
            "user_query": user_query,
        }

        prompt_inputs["chat_history"] = []

        response = self.chain.invoke(prompt_inputs, config=config)

        return response.content if hasattr(response, 'content') else str(response)

class UserInteractionHandler:
    """Handles user inputs like 'Show me my data.'"""

    def __init__(self, user_query_chain, user_response_chain):
        self.user_query_chain = user_query_chain
        self.user_response_chain = user_response_chain

    def handle_input(self, user_input, user_id):
        """Process the user input to fetch and display user data."""
        query_result = self.user_query_chain.invoke({"user_id": user_id})

        response = self.user_response_chain.invoke(
            {
                "user_data": query_result,
                "user_query": user_input,
            },
            config={},
        )

        return response
    

