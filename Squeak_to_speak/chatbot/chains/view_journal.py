# User intention: I Want to See My Journal

# Chain 1: Retrieve Journal Entries
# Goal: Retrieve the journal entries the user wants to see.
# Implementation: This chain queries the database for journal entries matching the user’s criteria, orders, and structures them as output.

class RetrieveJournalEntries:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_entries(self, user_input):
        """
        Retrieves journal entries based on user-provided filters (e.g., time range, tags).
        """
        try:
            query = """
            SELECT entry_id, content, created_at
            FROM Journal_entries
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


# Chain 2: Present Journal Entries
# Goal: Present the retrieved journal entries to the user.
# Implementation: This chain formats and structures the retrieved entries into a user-friendly output.

class PresentJournalEntries:
    def format_output(self, retrieval_result):
        """
        Formats the retrieved journal entries for user-friendly presentation.
        """
        if "error" in retrieval_result:
            return f"An error occurred: {retrieval_result['error']}"

        entries = retrieval_result.get("entries", [])
        if not entries:
            return "You have no journal entries to display."

        formatted_entries = "\n".join(
            [
                f"Entry ID: {entry['entry_id']}\nDate: {entry['created_at']}\nContent: {entry['content']}\n"
                for entry in entries
            ]
        )
        return f"Here are your journal entries:\n\n{formatted_entries}"