# User Story: I want to share details about a habit I wish to change to receive practical and quick suggestions with healthier alternatives.

# Preparation
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import pinecone
import os
from dotenv import load_dotenv


load_dotenv()
pinecone_api_key = os.getenv('PINECONE_API_KEY')

class RoutineAlternativesIndexer:
    def __init__(self, pinecone_api_key, pinecone_env):
        # Initialize Pinecone and embedding model
        pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index_name = "routine-alternatives"

        # Create Pinecone index if not exists
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(self.index_name, dimension=384)

        self.index = pinecone.Index(self.index_name)

    def index_pdf(self, pdf_path):
        reader = PdfReader(pdf_path)
        content = ""
        for page in reader.pages:
            content += page.extract_text()

        sentences = [sentence.strip() for sentence in content.split(".") if sentence.strip()]
        embeddings = self.embedding_model.encode(sentences)
        
        # Upsert sentences into Pinecone
        for i, embedding in enumerate(embeddings):
            self.index.upsert([(str(i), embedding.tolist(), {"text": sentences[i]})])

        return "PDF content indexed successfully."

# Example usage:
# indexer = RoutineAlternativesIndexer("your-pinecone-api-key", "your-pinecone-environment")
# print(indexer.index_pdf("Squeak_to_speak/data/pdfs/Dangerous routines alternatives.pdf"))


# Chain 1
# Goal: Use RAG to retrieve an appropriate routine alternative
# Implementation: This Chain queries an embedding database (Pinecone) for relevant routines. Retrieved routines are ranked for relevance and utility.
class RoutineAlternativeRetriever:
    def __init__(self, pinecone_api_key, pinecone_env):
        # Initialize Pinecone and embedding model
        pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = pinecone.Index("routine-alternatives")

    def find_alternatives(self, user_input):
        # Generate embedding for user input
        query_embedding = self.embedding_model.encode(user_input)
        results = self.index.query(query_embedding.tolist(), top_k=5, include_metadata=True)

        # Extract relevant routines
        alternatives = [match["metadata"]["text"] for match in results["matches"]]
        return alternatives


# Chain 2
# Goal: Output response
# Implementation: This chain receives both inputs (user input and most relevant documents) and generates a final output using a prompt template.
class RoutineAlternativeOutputFormatter:
    def format_output(self, user_input, alternatives):
        if alternatives:
            response = (
                f"Based on your input, here are some healthier alternatives to '{user_input}':\n"
            )
            response += "\n".join(f"- {alt}" for alt in alternatives)
            return response
        return "Sorry, no relevant alternatives were found at this time."
