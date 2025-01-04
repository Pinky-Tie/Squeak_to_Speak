import datetime
from pydantic import BaseModel
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from data.database_functions import DatabaseManager

# User Story: I want to anonymously share something I’m grateful and/or happy for so that I can help brighten someone else’s day while fostering my own positivity.

# Chain 1
# Goal: Insert the users' gratitude message into the database
# Implementation: This chain transforms the user’s input into an object that can be inserted into the database. The Chain ends with confirmation of insertion from the database.

# GratitudeEntry model
class GratitudeEntry(BaseModel):
    date: str
    comment: str

# Reasoning Chain
class GratitudeEntryManager:
    def __init__(self, db_manager:DatabaseManager):
        self.db_manager = db_manager

    def process(self, message:str) -> dict[str, str]:
        """
        Extracts variables from user message and inserts them into the database.
        """

        # Get current date
        date = datetime.now().strftime("%Y-%m-%d")

        # Create journal entry object
        entry = GratitudeEntry(
            date = date,
            comment = message
        )

        # Insert into the database
        success = self.db_manager.insert("Gratitude_entries", entry.dict())
        return {"success": success}

# Chain 2
# Goal: Inform the user that the entry has been inserted
# Implementation: This chain receives the user input and generates a final output using a prompt template.

class GratitudeEntryResponse:
    def generate(self, success: bool) -> str:
        """
        Generates a response based on the success of the database operation.
        """
        if success:
            return "Your gratitude entry has been successfully added."
        else:
            return "There was an error adding your gratitude entry. Please try again later."