# User intention: I Want to See My Journal

# Chain 1: Retrieve Journal Entries
# Goal: Retrieve the journal entries the user wants to see.
# Implementation: This chain queries the database for journal entries matching the user’s criteria, orders, and structures them as output.
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
class JournalEntry(BaseModel):
    """Model for representing a journal entry."""
    user_id: int = Field(..., description="User ID")
    message: str = Field(..., description="message")

class JournalQueryResult(BaseModel):
    """Model for the result containing multiple journal entries."""
    results: List[JournalEntry]

class JournalQueryChain(Runnable):
    """Chain for querying Journal entries from a database based on user ID."""

    def retrieve_journal(self, user_id=1, limit=5):
        """Fetch a specified number of Journal entries for a given user ID."""
        conn, cursor = connect_database()

        try:
            query = """
            SELECT message
            FROM Journal
            WHERE user_id = ?
            LIMIT ?;
            """
            cursor.execute(query, (user_id, limit))
            rows = cursor.fetchall()
        finally:
            conn.close()

        # Convert rows into JournalEntry objects
        results = [JournalEntry(user_id=user_id, message=row[0]) for row in rows]
        return results

    def invoke(self, inputs):
        """Invoke the chain to query Journal entries."""
        user_id = inputs.get("user_id")
        limit = inputs.get("limit", 5)

        # Fetch Journal entries
        journal_entries = self.retrieve_journal(user_id=user_id, limit=limit)

        # If no entries are found, return an appropriate message
        if not journal_entries:
            return {"message": "No journal entries found for the given user."}

        # Format the output
        output = JournalQueryResult(results=journal_entries)
        return output



class JournalResponseChain(Runnable):
    """Chain that generates a response to a journal query."""

    def __init__(self, llm, memory=True):
        """Initialize the journal response chain."""
        super().__init__()
        self.llm = llm

        # Define the prompt template for customer service interaction
        prompt_template = PromptTemplate(
            system_template="""
            You are a journal assistant capable of retrieving and summarizing user journal entries.
            Your task is to present the retrieved journal entries in a clear and organized manner.

            Guidelines:
            1. Provide a concise summary of the entries.
            2. Show empathy and understanding in the tone.
            3. Offer additional assistance if the user requires further support.
            
            Retrieved Journal Entries:
            {journal_entries}
            """,
            human_template="""
            User Query:
            {user_query}
            """,
        )

        self.prompt = generate_prompt_templates(prompt_template, memory=memory)
        self.chain = self.prompt | self.llm

    def invoke(self, inputs, config):
        """Invoke the journal response chain."""
        journal_entries = inputs.get("journal_entries")
        user_query = inputs.get("user_query")

        # Combine inputs for the prompt
        prompt_inputs = {
            "journal_entries": json.dumps(
                [entry.dict() for entry in journal_entries], indent=4
            ),
            "user_query": user_query,
        }

        # Add an empty chat_history to avoid errors
        prompt_inputs["chat_history"] = []

        # Get the response from the chain
        response = self.chain.invoke(prompt_inputs, config=config)

        # Directly access the `content` attribute of the response
        return response.content if hasattr(response, 'content') else str(response)



class JournalInteractionHandler:
    """Handles user inputs like 'let me view my Journal entries'."""

    def __init__(self, journal_query_chain, journal_response_chain):
        self.journal_query_chain = journal_query_chain
        self.journal_response_chain = journal_response_chain

    def handle_input(self, user_input, user_id):
        """Process the user input to fetch and display Journal entries."""

        # Query the Journal entries
        query_result = self.journal_query_chain.invoke({"user_id": user_id, "limit": 5})

        # Check if no entries are found
        if "message" in query_result:
            return query_result["message"]

        # Generate a response
        response = self.journal_response_chain.invoke(
            {
                "journal_entries": query_result.results,
                "user_query": user_input,
            },
            config={},
        )

        return response