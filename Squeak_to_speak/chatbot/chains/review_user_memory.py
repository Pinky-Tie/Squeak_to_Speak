# User Story: I want to review the data Squeak to Speak holds about me to better understand what is collected and how it is used.

# Chain 1
# Goal: Retrieve information on the user
# Implementation: This chain takes the user’s input, defines a time window for retrieval of the data and queries the database for all relevant entries inside that time window. It will then structure the information and output it.
from typing import List, Dict
from datetime import datetime

class RetrieveUserData:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def retrieve_user_info(self, user_id: int) -> Dict:
        """
        Retrieves user information from the user database.
        """
        query = """
        SELECT * FROM Users
        WHERE user_id = :user_id
        """
        params = {"user_id": user_id}
        result = self.db_manager.fetch_one(query, params)
        return result if result else {"error": "No user information found."}

    def retrieve_journal_entries(self, user_id: int, start_date: str = None, end_date: str = None) -> List[Dict]:
        """
        Retrieves journal entries for the user within the specified date range.
        If no date range is specified, all journal entries for the user are retrieved.
        """
        if not start_date:
            start_date = '2024-12-01'
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')

        query = """
        SELECT * FROM Journal_entries
        WHERE user_id = :user_id AND created_at BETWEEN :start_date AND :end_date
        """
        params = {
            "user_id": user_id,
            "start_date": start_date,
            "end_date": end_date,
        }
        results = self.db_manager.fetch_all(query, params)
        return results if results else []

    def retrieve_mood_board_entries(self, user_id: int, start_date: str = None, end_date: str = None) -> List[Dict]:
        """
        Retrieves mood board entries for the user within the specified date range.
        If no date range is specified, all mood board entries for the user are retrieved.
        """
        if not start_date:
            start_date = '1970-01-01'
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')

        query = """
        SELECT * FROM Mood_board_entries
        WHERE user_id = :user_id AND created_at BETWEEN :start_date AND :end_date
        """
        params = {
            "user_id": user_id,
            "start_date": start_date,
            "end_date": end_date,
        }
        results = self.db_manager.fetch_all(query, params)
        return results if results else []

    def retrieve_data(self, user_id: int, start_date: str = None, end_date: str = None) -> Dict:
        """
        Retrieves all relevant data for the user, including user information, journal entries, and mood board entries.
        """
        user_info = self.retrieve_user_info(user_id)
        journal_entries = self.retrieve_journal_entries(user_id, start_date, end_date)
        mood_board_entries = self.retrieve_mood_board_entries(user_id, start_date, end_date)

        return {
            "user_info": user_info,
            "journal_entries": journal_entries,
            "mood_board_entries": mood_board_entries
        }