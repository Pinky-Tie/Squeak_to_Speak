# User intention: I Want to See My Mood Board

# Chain 1: Retrieve Mood Board Entries
# Goal: Retrieve the mood board entries the user wants to see.
# Implementation: This chain queries the database for mood board entries matching the user’s criteria, orders, and structures them as output.

class RetrieveMoodBoardEntries:
    def __init__(self, db_manager, rag_pipeline):
        self.db_manager = db_manager
        self.rag_pipeline = rag_pipeline

    def prompt_for_search_type(self) -> str:
        """
        Prompt the user to choose between searching by date or topic.
        """
        return "Do you want to search by date or topic? Please type 'date' or 'topic'."

    def prompt_for_date(self) -> str:
        """
        Prompt the user to enter the date of the mood board entry they want to view.
        """
        return "Enter the date of the mood board entry you want to view, in format (YYYY-MM-DD): "

    def prompt_for_topic(self) -> str:
        """
        Prompt the user to enter the topic of the mood board entry they want to view.
        """
        return "Enter the topic of the mood board entry you want to view: "

    def get_entries_by_date(self, user_id: int, date: str):
        """
        Retrieves mood board entries based on the specified date.
        """
        try:
            query = """
            SELECT entry_id, content, date
            FROM Mood_board_entries
            WHERE user_id = :user_id AND date = :date
            ORDER BY date DESC
            """
            params = {
                "user_id": user_id,
                "date": date,
            }
            results = self.db_manager.fetch_all(query, params)
            return {"entries": results} if results else {"error": "No entries found for the specified date."}
        except Exception as e:
            return {"error": str(e)}

    def get_entries_by_topic(self, user_id: int, topic: str):
        """
        Retrieves mood board entries based on the specified topic using RAG.
        """
        try:
            query = f"Find mood board entries about {topic} for user {user_id}"
            response = self.rag_pipeline.rag_chain.invoke({"customer_input": query})
            return {"entries": response} if response else {"error": "No entries found for the specified topic."}
        except Exception as e:
            return {"error": str(e)}

# Chain 2: Present Mood Board Entries
# Goal: Present the retrieved mood board entries to the user.
# Implementation: This chain formats the retrieved entries and presents them to the user.
class PresentMoodBoardEntries:
    def format_output(self, entries):
        """
        Formats the retrieved mood board entries for presentation.
        """
        if "error" in entries:
            return entries["error"]
        
        formatted_entries = "\n".join([f"Date: {entry['created_at']}\nContent: {entry['content']}" for entry in entries["entries"]])
        return formatted_entries if formatted_entries else "No entries found for the specified date or topic."