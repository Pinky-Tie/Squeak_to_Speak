from datetime import datetime
from pydantic import BaseModel
from data.database_functions import DatabaseManager

class MoodEntry(BaseModel):
    user_id: int
    mood: str
    date: str

# Chain 1
# Goal: Retrieve the entries the users want to see
# Implementation: This chain queries the database for matching entries, ordering and structuring them as output.
class MoodEntryManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def process(self, user_id: int, mood: str) -> dict[str, str]:
        """
        Extracts variables from user message and inserts them into the database.
        """

        # Check if the mood entry is too long
        if len(mood) > 20:
            return {"error": "The mood entry is too long. Please create a journal entry instead."}

        # Get current date
        date = datetime.now().strftime("%Y-%m-%d")

        # Check if an entry already exists for the given date
        query = """
        SELECT mood_id
        FROM Mood_tracker
        WHERE user_id = :user_id AND date = :date
        """
        params = {"user_id": user_id, "date": date}
        result = self.db_manager.select(query, params)
        if result:
            return {"error": "A mood entry already exists for today. Please update the existing entry or wait until tomorrow."}

        # Create mood entry object
        entry = MoodEntry(
            user_id=user_id,
            mood=mood,
            date=date
        )

        # Insert into the database
        success = self.db_manager.insert("Mood_tracker", entry.dict())
        return {"success": success}

# Chain 2
# Goal: Present these entries to the user
# Implementation: This chain receives all inputs (user input and structured entries) and generates a final output using a prompt template.
class MoodEntryResponse:
    def generate(self, result: dict) -> str:
        """Generates a response based on the success of the database operation."""
        if "error" in result:
            return result["error"]
        if result["success"]:
            return "Your mood entry has been successfully added."
        else:
            return "There was an error adding your mood entry. Please try again later."