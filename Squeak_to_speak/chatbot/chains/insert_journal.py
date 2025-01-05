import os
import sys
from datetime import datetime
from pydantic import BaseModel
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from data.database_functions import DatabaseManager

class JournalEntry(BaseModel):
    user_id: int
    message: str
    date: str
    hide_yn: bool

# Reasoning Chain
class JournalEntryManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def process(self, user_id: int, user_message: str) -> dict[str, str]:
        """Extracts variables from user message and inserts them into the database."""
        # Default hide_yn to False
        hide_yn = 'hide' in user_message.lower()

        # Get current date
        date = datetime.now().strftime("%Y-%m-%d")

        # Check if an entry already exists for the given date
        query = """
        SELECT message_id
        FROM Journal
        WHERE user_id = :user_id AND date = :date
        """
        params = {"user_id": user_id, "date": date}
        result = self.db_manager.select(query, params)
        if result:
            return {"error": "A journal entry already exists for today. Please update the existing entry or wait until tomorrow."}

        # Create journal entry object
        entry = JournalEntry(
            user_id=user_id,
            message=user_message,
            date=date,
            hide_yn=hide_yn
        )

        # Insert into the database
        success = self.db_manager.insert("Journal", entry.dict())
        return {"success": success}

# Response Chain
class JournalEntryResponse:
    def generate(self, result: dict) -> str:
        """Generates a response based on the success of the database operation."""
        if "error" in result:
            return result["error"]
        if result["success"]:
            return "Your journal entry has been successfully added."
        else:
            return "There was an error adding your journal entry. Please try again later."