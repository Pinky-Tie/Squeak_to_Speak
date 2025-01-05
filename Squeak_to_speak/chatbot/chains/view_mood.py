# User intention: I Want to See My Mood Board

# Chain 1: Retrieve Mood Board Entries
# Goal: Retrieve the mood board entries the user wants to see.
# Implementation: This chain queries the database for mood board entries matching the user’s criteria, orders, and structures them as output.
from langchain import callbacks
from langchain.output_parsers import PydanticOutputParser
from langchain.schema.runnable.base import Runnable
from pydantic import BaseModel, Field
from typing import List, Optional
# Define the product database as a dictionary with product categories
import sys
import os
import json
from langchain_openai import ChatOpenAI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from data.data_func import connect_database
from chatbot.chains.base import PromptTemplate, generate_prompt_templates

import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")




# Base Models for data handling using Pydantic
class MoodEntry(BaseModel):
    """Model for representing a Mood entry."""
    user_id: int = Field(..., description="User ID")
    mood: str = Field(..., description="mood")

class MoodQueryResult(BaseModel):
    """Model for the result containing multiple Mood entries."""
    results: List[MoodEntry]

class MoodQueryChain(Runnable):
    """Chain for querying Mood entries from a database based on user ID."""

    def retrieve_Mood(self, user_id=1, limit=5):
        """Fetch a specified number of Mood comments for a given user ID."""
        conn, cursor = connect_database()

        try:
            query = """
            SELECT mood
            FROM Mood_tracker
            WHERE user_id = ?
            LIMIT ?;
            """
            cursor.execute(query, (user_id, limit))
            rows = cursor.fetchall()
        finally:
            conn.close()

        # Convert rows into MoodEntry objects
        results = [MoodEntry(user_id=user_id, mood=row[0]) for row in rows]
        return results

    def invoke(self, inputs):
        """Invoke the chain to query Mood entries."""
        user_id = inputs.get("user_id")
        limit = inputs.get("limit", 5)

        # Fetch Mood entries
        Mood_entries = self.retrieve_Mood(user_id=user_id, limit=limit)

        # Format the output
        output = MoodQueryResult(results=Mood_entries)
        return output


class MoodResponseChain(Runnable):
    """Chain that generates a response to a Mood query."""

    def __init__(self, llm, memory=True):
        """Initialize the Mood response chain."""
        super().__init__()
        self.llm = llm

        # Define the prompt template for customer service interaction
        prompt_template = PromptTemplate(
            system_template="""
            You are a Mood assistant capable of retrieving and summarizing user Mood entries.
            Your task is to present the retrieved Mood entries in a clear and organized manner.

            Guidelines:
            1. Provide a concise summary of the entries.
            2. Show empathy and understanding in the tone.
            3. Offer additional assistance if the user requires further support.
            
            Retrieved Mood Entries:
            {Mood_entries}
            """,
            human_template="""
            User Query:
            {user_query}
            """,
        )

        self.prompt = generate_prompt_templates(prompt_template, memory=memory)
        self.chain = self.prompt | self.llm

    def invoke(self, inputs, config):
        """Invoke the mood response chain."""
        mood_entries = inputs.get("mood_entries")
        user_query = inputs.get("user_query")

        # Combine inputs for the prompt
        prompt_inputs = {
            "mood_entries": json.dumps(
                [entry.dict() for entry in mood_entries], indent=4
            ),
            "user_query": user_query,
        }

        # Add an empty chat_history to avoid errors
        prompt_inputs["chat_history"] = []

        # Get the response from the chain
        response = self.chain.invoke(prompt_inputs, config=config)

        # Directly access the `content` attribute of the response
        return response.content if hasattr(response, 'content') else str(response)


class MoodInteractionHandler:
    """Handles user inputs like 'let me view my Mood entries'."""

    def __init__(self, Mood_query_chain, Mood_response_chain):
        self.Mood_query_chain = Mood_query_chain
        self.Mood_response_chain = Mood_response_chain

    def handle_input(self, user_input, user_id):
        """Process the user input to fetch and display Mood entries."""
            # Query the Mood entries
        query_result = self.Mood_query_chain.invoke({"user_id": user_id, "limit": 5})

        # Generate a response
        response = self.Mood_response_chain.invoke(
            {
                "Mood_entries": query_result.results,
                "user_query": user_input,
            },
            config={},
        )

        return response



# Example Usage
# Create chains for querying and responding
'''Mood_query_chain = MoodQueryChain()
Mood_response_chain = MoodResponseChain(llm=ChatOpenAI(temperature=0.0, model="gpt-4o-mini"))
Mood_handler = MoodInteractionHandler(Mood_query_chain, Mood_response_chain)

# Example user input and handling
user_input = "Let me view my moods"
user_id = 1  # Assume this is retrieved from the session or context
response = Mood_handler.handle_input(user_input = user_input, user_id = user_id)
print(response)'''