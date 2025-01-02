# User intention: I Want to See My Mood Board

# Chain 1: Retrieve Mood Board Entries
# Goal: Retrieve the mood board entries the user wants to see.
# Implementation: This chain queries the database for mood board entries matching the user’s criteria, orders, and structures them as output.

class RetrieveMoodBoardEntries:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_entries(self, user_input):
        """
        Retrieves mood board entries based on user-provided filters (e.g., time range, themes).
        """
        try:
            query = """
            SELECT entry_id, content, created_at
            FROM Mood_board_entries
            WHERE user_id = :user_id
            AND (:start_date IS NULL OR created_at >= :start_date)
            AND (:end_date IS NULL OR created_at <= :end_date)
            ORDER BY created_at DESC
            """
            params = {
                "user_id": user_input.get("user_id"),
                "start_date": user_input.get("start_date"),
                "end_date": user_input.get("end_date"),
            }
            results = self.db_manager.fetch_all(query, params)
            return {"entries": results} if results else {"error": "No entries found."}
        except Exception as e:
            return {"error": str(e)}
        

# Chain 2: Present Mood Board Entries
# Goal: Present the retrieved mood board entries to the user.
# Implementation: This chain formats and structures the retrieved entries into a user-friendly output.

class PresentMoodBoardEntries:
    def format_output(self, retrieval_result):
        """
        Formats the retrieved mood board entries for user-friendly presentation.
        """
        if "error" in retrieval_result:
            return f"An error occurred: {retrieval_result['error']}"

        entries = retrieval_result.get("entries", [])
        if not entries:
            return "You have no mood board entries to display."

        formatted_entries = "\n".join(
            [
                f"Entry ID: {entry['entry_id']}\nDate: {entry['created_at']}\nContent: {entry['content']}\n"
                for entry in entries
            ]
        )
        return f"Here are your mood board entries:\n\n{formatted_entries}"