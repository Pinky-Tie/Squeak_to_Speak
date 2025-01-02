# User Story: I want to communicate with Squeak to Speak’s assistant, leveraging its understanding of my journal and mood board to create more empathetic interactions.

# Chain 1
# Goal: Use RAG to retrieve information related to the users' input
# Implementation: This chain queries an embedding database (Pinecone) for relevant entries. Retrieved entries are ranked for relevance and utility.
from typing import List, Dict
import pinecone
import os
from dotenv import load_dotenv


load_dotenv()
pinecone_api_key = os.getenv('PINECONE_API_KEY')

class RetrieveRelevantEntries:
    def __init__(self, pinecone_index, embedding_model, db_manager):
        self.pinecone_index = pinecone_index
        self.embedding_model = embedding_model
        self.db_manager = db_manager

    def query_relevant_entries(self, user_input: str, top_k: int = 3) -> List[Dict]:
        """
        Queries the Pinecone index for relevant entries based on the user's input.
        Returns the top_k most relevant entries.
        """
        # Generate embedding for the user input
        query_embedding = self.embedding_model.encode(user_input)
        
        # Query Pinecone index for relevant entries
        query_results = self.pinecone_index.query(
            query_embedding,
            top_k=top_k,
            include_values=True,
            include_metadata=True
        )
        
        # Extract and return the relevant entries (text and metadata)
        return [
            {"entry_id": result.id, "text": result.metadata['text'], "score": result.score}
            for result in query_results.matches
        ]

    def get_entries_by_date(self, user_id, entry_type, start_date=None, end_date=None):
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

        return self.db_manager.select(query, params)


# Chain 2
# Goal: Give the user the response to the question made
# Implementation: This chain receives both inputs (most relevant documents and user input) and generates a final user output using a prompt template.
from typing import Dict

class GenerateEmpatheticResponse:
    def __init__(self, prompt_template):
        self.prompt_template = prompt_template

    def generate_response(self, relevant_entries: List[Dict], user_input: str) -> str:
        """
        Generates an empathetic response using the retrieved entries and the user input.
        """
        # Combine retrieved entries into a coherent response prompt
        entry_texts = "\n".join([entry['text'] for entry in relevant_entries])
        prompt = self.prompt_template.format(user_input=user_input, entries=entry_texts)
        
        # Here, you would pass the prompt to a model (like GPT) to generate a response.
        # For now, we simulate generating a response.
        empathetic_response = self.simulate_generation(prompt)
        
        return empathetic_response

    def simulate_generation(self, prompt: str) -> str:
        """
        Simulates the generation of a response from an LLM.
        In a real scenario, you would call a language model API here.
        """
        return f"Here's an empathetic response based on your input: {prompt}"
