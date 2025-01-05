# User Story: I want to document my thoughts and feelings in a private journal or mood board to reflect, vent or track my mental health journey in a safe space.

import datetime
import sys
from pydantic import BaseModel

import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from data.database_functions import DatabaseManager
class JournalEntry(BaseModel):
    user_id: int
    message: str
    date: str
    hide_yn: bool
    time: str

# Reasoning Chain
class JournalEntryManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def process(self, user_id: int, user_message: str) -> dict[str, str]:
        """Extracts variables from user message and inserts them into the database."""
        # Default hide_yn to False
        hide_yn = 'hide' in user_message.lower()

        # Get current date and time
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")

        print(user_message)
        # Create journal entry object
        entry = JournalEntry(
            user_id=int(user_id),
            message=user_message,
            date=date,
            hide_yn=hide_yn
        )

        # Insert into the database
        success = self.db_manager.insert("Journal", entry.dict())
        return {"success": success}

# Response Chain
class JournalEntryResponse:
    def generate(self, success: bool) -> str:
        """Generates a response based on the success of the database operation."""
        if success:
            return "Your journal entry has been successfully added."
        else:
            return "There was an error adding your journal entry. Please try again later."
