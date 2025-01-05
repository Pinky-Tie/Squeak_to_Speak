# User Story: I want to modify entries in my journal to correct errors and make necessary updates.

from data.database_functions import DatabaseManager

# Chain 1
# Goal: Identify which entry the user wants to modify
# Implementation: This chain identifies the query the user wishes to alter and outputs it as an object.
class IdentifyJournalEntryToModify:
    def get_entry_to_modify(self, user_id: int, date: str, db_manager: DatabaseManager):
        """
        Retrieves the journal entry for the specified date.
        """
        query = """
        SELECT entry_id, content
        FROM Journal
        WHERE user_id = :user_id AND entry_date = :entry_date
        """
        params = {"user_id": user_id, "entry_date": date}
        result = db_manager.select(query, params)
        if result:
            return result[0]
        return None

# Chain 2
# Goal: Alter the entry with the users' inputs
# Implementation: This chain takes as input the entry to be altered and the user input, structures the new values for the entry and alters it, outputting confirmation for the alteration.
class ModifyJournalEntry:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def prompt_for_new_content(self) -> str:
        """
        Prompt the user to enter the new content for the journal entry.
        """
        return "Enter the new content for the journal entry: "

    def modify_entry(self, entry_id: int, updated_content: str):
        """
        Updates the journal entry with the provided content.
        """
        query = """
        UPDATE Journal
        SET content = :updated_content, updated_at = CURRENT_TIMESTAMP
        WHERE entry_id = :entry_id
        """
        params = {"entry_id": entry_id, "updated_content": updated_content}
        success = self.db_manager.execute(query, params)
        return {"success": success} if success else {"error": "Failed to update the entry."}

# Chain 3
# Goal: Inform the user that the entry has been changed
# Implementation: This chain receives both inputs (user input and alteration confirmation) and generates a final output using a prompt template.
class InformUserOfJournalChange:
    def format_output(self, modification_result):
        """
        Formats the result of the modification to inform the user.
        """
        if "error" in modification_result:
            return f"An error occurred: {modification_result['error']}"

        return "Your journal entry has been successfully updated."