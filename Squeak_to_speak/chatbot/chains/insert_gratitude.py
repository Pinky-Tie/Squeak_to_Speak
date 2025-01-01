import datetime
# User Story: I want to anonymously share something I’m grateful and/or happy for so that I can help brighten someone else’s day while fostering my own positivity.

# Chain 1
# Goal: Insert the users' gratitude message into the database
# Implementation: This chain transforms the user’s input into an object that can be inserted into the database. The Chain ends with confirmation of insertion from the database.

class GratitudeManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_gratitude_message(self, comment):
        # Validates and adds a gratitude message to the database.
        if not comment or len(comment.strip()) == 0:
            return "Your gratitude message cannot be empty."

        data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "comment": comment,
        }

        # Attempt to insert the gratitude message into the database
        success = self.db_manager.insert("Gratitude_entries", data)

        # Chain 2
        # Goal: Inform the user that the entry has been inserted
        # Implementation: This chain receives the user input and generates a final output using a prompt template.

        if success:
            return "Your gratitude message has been added successfully!"
        else:
            return "An error occurred. Please try again."