# User Story: I want to delete entries from my journal to maintain control over the information stored about me.

# Chain 1
# Goal: Delete the entry the user has requested to be deleted
# Implementation: This chain identifies the entry the user wishes to delete and deletes it, outputting confirmation from the database.
class JournalEntryDeleter:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def delete_entry(self, user_id: int, entry_id: int):
        """Delete a specific journal entry for the user."""
        query = """
        DELETE FROM Journal_entries
        WHERE user_id = :user_id AND entry_id = :entry_id
        RETURNING entry_id
        """
        params = {
            "user_id": user_id,
            "entry_id": entry_id,
        }
        result = self.db_manager.execute(query, params)
        return result


# Chain 2
# Goal: Inform the user that the entry has been deleted
# Implementation: This chain receives both inputs (user input and deletion confirmation) and generates a final output using a prompt template.
class DeletionConfirmationFormatter:
    def format_output(self, deletion_result, entry_id):
        """Generate a message confirming the deletion."""
        if deletion_result:
            return f"Journal entry with ID {entry_id} has been successfully deleted."
        return f"Unable to delete the journal entry with ID {entry_id}. Please ensure the entry ID is correct."
