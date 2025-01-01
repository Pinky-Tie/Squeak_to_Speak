# User Story: I want to review the data Squeak to Speak holds about me to better understand what is collected and how it is used.

# Chain 1
# Goal: Retrieve information on the user
# Implementation: This chain takes the user’s input, defines a time window for retrieval of the data and queries the database for all relevant entries inside that time window. It will then structure the information and output it.
from typing import List, Dict
from datetime import datetime

class RetrieveUserData:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def retrieve_data(self, user_id: int, start_date: str = None, end_date: str = None) -> List[Dict]:
        """
        Retrieves relevant entries from the database for the user within the specified date range.
        If no date range is specified, all data for the user is retrieved.
        """
        # If no dates are provided, use the current date as the range
        if not start_date:
            start_date = datetime.now().strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Query the database for journal and mood board entries in the given date range
        query = """
        SELECT * FROM Journal_entries
        WHERE user_id = :user_id AND created_at BETWEEN :start_date AND :end_date
        UNION
        SELECT * FROM Mood_board_entries
        WHERE user_id = :user_id AND created_at BETWEEN :start_date AND :end_date
        """
        params = {
            "user_id": user_id,
            "start_date": start_date,
            "end_date": end_date,
        }
        
        # Fetch the data from the database
        journal_results = self.db_manager.select(query, params)
        
        return journal_results


# Chain 2
# Goal: Present information to the user
# Implementation: This chain receives as inputs the user input, user information and chat memory and generates a final output using a prompt template.
class PresentUserData:
    def __init__(self, prompt_template: str):
        self.prompt_template = prompt_template

    def format_data(self, user_input: str, retrieved_data: List[Dict]) -> str:
        """
        Formats the retrieved user data into a readable output using a prompt template.
        """
        # Structure the retrieved data for display
        formatted_data = "\n".join([f"Entry: {entry['entry_text']} | Date: {entry['created_at']}" for entry in retrieved_data])
        
        # Generate the final prompt to present the data to the user
        prompt = self.prompt_template.format(user_input=user_input, data=formatted_data)
        
        return prompt
