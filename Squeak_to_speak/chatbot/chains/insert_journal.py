# User Story: I want to document my thoughts and feelings in a private journal or mood board to reflect, vent or track my mental health journey in a safe space.

# Chain 1
# Goal: Insert journal entry into the user’s journal or mood board on the database
# Implementation: This chain validates the user input, structures it for input in the database and completes that same input, finishing the process when it receives confirmation from the database.
from .base import PromptTemplate as PromptT
from .base import  generate_prompt_templates
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
import datetime






# JournalEntry model
class JournalEntry(BaseModel):
    user_id: int
    message: str
    date: str
    hide_yn: bool
    time: str

# DatabaseManager provided in the prompt
class DatabaseManager:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, table_name, data):
        placeholders = ", ".join(f":{key}" for key in data.keys())
        columns = ", ".join(data.keys())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, data)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting into {table_name}: {e}")
            return False
        finally:
            cursor.close()

# Reasoning Chain
class JournalManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def process(self, user_id: int, user_message: str) -> dict[str, str]:
        """Extracts variables from user message and inserts them into the database."""
        # Default hide_yn to False
        hide_yn = 'hide' in user_message.lower()

        # Get current date and time
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M")

        # Create journal entry object
        entry = JournalEntry(
            user_id=user_id,
            message=user_message,
            date=date,
            hide_yn=hide_yn,
            time=time
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
