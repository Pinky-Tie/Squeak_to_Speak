# User Story: I want to modify entries in my journal to correct errors and make necessary updates.

# Chain 1
# Goal: Identify which entry the user wants to modify
# Implementation: This chain identifies the query the user wishes to alter and outputs it as an object.
class IdentifyJournalEntryToModify:
    def get_entry_to_modify(self, user_input):
        """
        Parses the user input to identify the journal entry the user wants to modify.
        Expects user_input to contain 'entry_id' and optional context.
        """
        try:
            entry_id = user_input.get("entry_id")
            if not entry_id:
                raise ValueError("Entry ID is required to modify an entry.")
            return {"entry_id": entry_id, "context": user_input.get("context")}
        except Exception as e:
            return {"error": str(e)}


# Chain 2
# Goal: Alter the entry with the users' inputs
# Implementation: This chain takes as input the entry to be altered and the user input, structures the new values for the entry and alters it, outputting confirmation for the alteration.
class ModifyJournalEntry:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def modify_entry(self, entry_id, updated_content):
        """
        Updates the journal entry with the provided content.
        """
        query = """
        UPDATE Journal_entries
        SET content = :updated_content, updated_at = CURRENT_TIMESTAMP
        WHERE entry_id = :entry_id
        """
        params = {"entry_id": entry_id, "updated_content": updated_content}

        success = self.db_manager.execute(query, params)
        return {"success": success, "entry_id": entry_id} if success else {"error": "Failed to update the entry."}


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

        return (
            f"Your journal entry with ID {modification_result['entry_id']} "
            f"has been successfully updated."
        )
