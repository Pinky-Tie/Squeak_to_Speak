# User intention: I Want to See My Journal

# Chain 1: Retrieve Journal Entries
# Goal: Retrieve the journal entries the user wants to see.
# Implementation: This chain queries the database for journal entries matching the user’s criteria, orders, and structures them as output.
from langchain import callbacks
from langchain.output_parsers import PydanticOutputParser
from langchain.schema.runnable.base import Runnable
from pydantic import BaseModel, Field
from base import PromptTemplate, generate_prompt_templates
from typing import List, Optional
# Define the product database as a dictionary with product categories
import sys
import os
import json
from langchain_openai import ChatOpenAI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from data.data_func import connect_database

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
    """Chain for querying journal entries from a database based on user ID."""

    def retrieve_journal(self, user_id=1, limit=5):
        """Fetch a specified number of journal comments for a given user ID."""
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
        """Invoke the chain to query journal entries."""
        user_id = inputs.get("user_id")
        limit = inputs.get("limit", 5)

        # Fetch journal entries
        journal_entries = self.retrieve_journal(user_id=user_id, limit=limit)

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
        prompt_inputs["chat_history"] = []  # This ensures compatibility

        return self.chain.invoke(prompt_inputs, config=config)


class JournalInteractionHandler:
    """Handles user inputs like 'let me view my journal entries'."""

    def __init__(self, journal_query_chain, journal_response_chain):
        self.journal_query_chain = journal_query_chain
        self.journal_response_chain = journal_response_chain

    def handle_input(self, user_input, user_id):
        """Process the user input to fetch and display journal entries."""
        if "journal entries" in user_input.lower():
            # Query the journal entries
            query_result = self.journal_query_chain.invoke({"user_id": user_id, "limit": 5})

            # Generate a response
            response = self.journal_response_chain.invoke(
                {
                    "journal_entries": query_result.results,
                    "user_query": user_input,
                },
                config={},
            )

            return response

        return "I'm sorry, I didn't understand your request. Can you clarify?"


# Example Usage
# Create chains for querying and responding
journal_query_chain = JournalQueryChain()
journal_response_chain = JournalResponseChain(llm=ChatOpenAI(temperature=0.0, model="gpt-4o-mini"))
journal_handler = JournalInteractionHandler(journal_query_chain, journal_response_chain)

# Example user input and handling
user_input = "Let me view my journal entries"
user_id = 1  # Assume this is retrieved from the session or context
response = journal_handler.handle_input(user_input = user_input, user_id = user_id)
print(response)

