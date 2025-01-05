import sys
import os
from pydantic import BaseModel

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from data.database_functions import DatabaseManager
class MoodEntry(BaseModel):
    user_id: int
    mood: str
    date: str
    description: str
import datetime

# User Story: I want to revisit past entries in my journal or mood board to reflect, recall and understand my experiences and emotions over time.

# Chain 1
# Goal: Retrieve the entries the users want to see
# Implementation: This chain queries the database for matching entries, ordering and structuring them as output.
class MoodEntryManager:
    def __init__(self, db_manager:DatabaseManager):
        self.db_manager = db_manager

    def process(self, user_id: int, mood: str) -> dict[str, str]:
        """
        Extracts variables from user message and inserts them into the database.
        """

        # Get current date
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        # Create journal entry object
        entry = MoodEntry(
                user_id = user_id,
                mood = mood,
                date = date)

        # Insert into the database
        success = self.db_manager.insert("Mood_tracker", entry.dict())
        return {"success": success}


# Chain 2
# Goal: Present these entries to the user
# Implementation: This chain receives all inputs (user input and structured entries) and generates a final output using a prompt template.
class MoodEntryResponse:
    def generate(self, success: bool) -> str:
        """Generates a response based on the success of the database operation."""
        if success:
            return "Your mood entry has been successfully added."
        else:
            return "There was an error adding your mood entry. Please try again later."
