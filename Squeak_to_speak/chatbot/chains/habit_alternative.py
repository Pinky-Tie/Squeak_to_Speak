# User Story: I want to share details about a habit I wish to change to receive practical and quick suggestions with healthier alternatives.

from PyPDF2 import PdfReader
import openai
import pinecone
import os
from dotenv import load_dotenv


load_dotenv()
pinecone_api_key = os.getenv('PINECONE_API_KEY')
openai_api_key = os.getenv("OPENAI_API_KEY")

class RoutineAlternativesIndexer:
    def __init__(self, pinecone_api_key, pinecone_env, openai_api_key):
        # Initialize Pinecone and OpenAI API
        pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
        openai.api_key = openai_api_key

        self.index_name = "routine-alternatives"

        # Create Pinecone index if not exists
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(self.index_name, dimension=1536)

        self.index = pinecone.Index(self.index_name)

    def _get_openai_embedding(self, text):
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response['data'][0]['embedding']

    def index_pdf(self, pdf_path):
        reader = PdfReader(pdf_path)
        content = ""
        for page in reader.pages:
            content += page.extract_text()

        sentences = [sentence.strip() for sentence in content.split(".") if sentence.strip()]
        embeddings = [self._get_openai_embedding(sentence) for sentence in sentences]

        # Upsert sentences into Pinecone
        for i, (sentence, embedding) in enumerate(zip(sentences, embeddings)):
            self.index.upsert([(str(i), embedding, {"text": sentence})])

        return "PDF content indexed successfully."


class RoutineAlternativeRetriever:
    def __init__(self, pinecone_api_key, pinecone_env, openai_api_key):
        # Initialize Pinecone and OpenAI API
        pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
        openai.api_key = openai_api_key

        self.index = pinecone.Index("routine-alternatives")

    def _get_openai_embedding(self, text):
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response['data'][0]['embedding']

    def find_alternatives(self, user_input):
        # Generate embedding for user input
        query_embedding = self._get_openai_embedding(user_input)
        results = self.index.query(query_embedding, top_k=5, include_metadata=True)

        # Extract relevant routines
        alternatives = [match["metadata"]["text"] for match in results["matches"]]
        return alternatives


class RoutineAlternativeOutputFormatter:
    def format_output(self, user_input, alternatives):
        if alternatives:
            response = (
                f"Based on your input, here are some healthier alternatives to '{user_input}':\n"
            )
            response += "\n".join(f"- {alt}" for alt in alternatives)
            return response
        return "Sorry, no relevant alternatives were found at this time."
