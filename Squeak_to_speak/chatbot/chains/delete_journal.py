# User Story: I want to delete entries from my journal to maintain control over the information stored about me.

from data.database_functions import DatabaseManager

# Chain 1
# Goal: Delete the entry the user has requested to be deleted
# Implementation: This chain identifies the entry the user wishes to delete and deletes it, outputting confirmation from the database.
class JournalEntryDeleter:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def prompt_for_date(self) -> str:
        """
        Prompt the user to enter the date of the journal entry they want to delete.
        """
        return "Enter the date you want to delete from, in format (YYYY-MM-DD): "

    def process(self, user_id: int, date = None):
        """
        Delete a specific journal entry for the user.
        """
        while date is None:
            # Prompt the user for the date if not provided
            date = input(self.prompt_for_date()).strip()
        
        query = """
        DELETE FROM Journal_entries
        WHERE user_id = :user_id AND entry_date = :entry_date
        RETURNING entry_id
        """
        params = {
            "user_id": user_id,
            "entry_date": date,
        }
        result = self.db_manager.execute(query, params)
        return result


# Chain 2
# Goal: Inform the user that the entry has been deleted
# Implementation: This chain receives both inputs (user input and deletion confirmation) and generates a final output using a prompt template.
class DeletionConfirmationFormatter:
    def format_output(self, deletion_result, entry_date):
        """Generate a message confirming the deletion."""
        if deletion_result:
            return f"Journal entry of {entry_date} has been successfully deleted."
        return f"I couldn't delete the journal entry of {entry_date}. Please check if the date is correct."