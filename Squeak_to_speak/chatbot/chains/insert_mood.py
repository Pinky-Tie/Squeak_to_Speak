# User Story: I want to revisit past entries in my journal or mood board to reflect, recall and understand my experiences and emotions over time.

# Chain 1
# Goal: Retrieve the entries the users want to see
# Implementation: This chain queries the database for matching entries, ordering and structuring them as output.
class RetrieveEntries:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_entries(self, user_id, entry_type, start_date=None, end_date=None):
        """
        Retrieves entries for the user based on the type (journal or mood board) and optional date range.
        """
        table_name = "Journal_entries" if entry_type == "journal" else "Moodboard_entries"

        query = f"""
        SELECT entry_id, content, created_at
        FROM {table_name}
        WHERE user_id = :user_id
        """
        params = {"user_id": user_id}

        if start_date:
            query += " AND created_at >= :start_date"
            params["start_date"] = start_date

        if end_date:
            query += " AND created_at <= :end_date"
            params["end_date"] = end_date

        query += " ORDER BY created_at ASC"

        return self.db_manager.select(query, params)


# Chain 2
# Goal: Present these entries to the user
# Implementation: This chain receives all inputs (user input and structured entries) and generates a final output using a prompt template.
class PresentEntries:
    def format_output(self, entries, entry_type):
        """
        Formats retrieved entries into a structured, user-friendly format.
        """
        if not entries:
            return f"No {entry_type} entries were found for the specified criteria."

        response = f"Here are your {entry_type} entries:\n\n"
        for entry in entries:
            response += (
                f"Entry ID: {entry['entry_id']}\n"
                f"Date: {entry['created_at']}\n"
                f"Content: {entry['content']}\n\n"
            )
        return response
