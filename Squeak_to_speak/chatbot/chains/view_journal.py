# User intention: I Want to See My Journal

# Chain 1: Retrieve Journal Entries
# Goal: Retrieve the journal entries the user wants to see.
# Implementation: This chain queries the database for journal entries matching the user’s criteria, orders, and structures them as output.

class RetrieveJournalEntries:
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
        Prompt the user to enter the date of the journal entry they want to view.
        """
        return "Enter the date of the journal entry you want to view, in format (YYYY-MM-DD): "

    def prompt_for_topic(self) -> str:
        """
        Prompt the user to enter the topic of the journal entry they want to view.
        """
        return "Enter the topic of the journal entry you want to view: "

    def get_entries_by_date(self, user_id: int, date: str):
        """
        Retrieves journal entries based on the specified date.
        """
        try:
            query = """
            SELECT entry_id, content, created_at
            FROM Journal_entries
            WHERE user_id = :user_id AND entry_date = :entry_date
            ORDER BY created_at DESC
            """
            params = {
                "user_id": user_id,
                "entry_date": date,
            }
            results = self.db_manager.fetch_all(query, params)
            return {"entries": results} if results else {"error": "No entries found for the specified date."}
        except Exception as e:
            return {"error": str(e)}

    def get_entries_by_topic(self, user_id: int, topic: str):
        """
        Retrieves journal entries based on the specified topic using RAG.
        """
        try:
            query = f"Find journal entries about {topic}"
            response = self.rag_pipeline.rag_chain.invoke({"customer_input": query})
            return {"entries": response} if response else {"error": "No entries found for the specified topic."}
        except Exception as e:
            return {"error": str(e)}

# Chain 2: Present Journal Entries
# Goal: Present the retrieved journal entries to the user.
# Implementation: This chain formats the retrieved entries and presents them to the user.
class PresentJournalEntries:
    def format_output(self, entries):
        """
        Formats the retrieved journal entries for presentation.
        """
        if "error" in entries:
            return entries["error"]
        
        formatted_entries = "\n".join([f"Date: {entry['created_at']}\nContent: {entry['content']}" for entry in entries["entries"]])
        return formatted_entries if formatted_entries else "No entries found for the specified date or topic."