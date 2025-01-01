# User Story: I want to document my thoughts and feelings in a private journal or mood board to reflect, vent or track my mental health journey in a safe space.

# Chain 1
# Goal: Insert journal entry into the user’s journal or mood board on the database
# Implementation: This chain validates the user input, structures it for input in the database and completes that same input, finishing the process when it receives confirmation from the database.

class JournalManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_entry(self, user_id, message, date, hide_yn, time):
        data = {
            "user_id": user_id,
            "message": message,
            "date": date,
            "hide_yn": hide_yn,
            "time": time,
        }
        return self.db_manager.insert("Journal", data)

# Chain 2
# Goal: Inform the user that the entry has been inserted
# Implementation: This chain receives the user input and generates a final output using a prompt template.

class JournalEntryResponse:
    def generate_response(self, success):
        return "Entry added successfully." if success else "Failed to add your entry."