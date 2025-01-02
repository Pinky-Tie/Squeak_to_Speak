# User Story: I want to learn more about Squeak to Speak as a company to build trust and confidence in its services.

# Chain 1
# Goal: Use RAG to retrieve information related to the users' input
# Implementation: This chain queries an embedding database (Pinecone) for relevant routines. Retrieved routines are ranked for relevance and utility.
import pinecone
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv


load_dotenv()
pinecone_api_key = os.getenv('PINECONE_API_KEY')

class RetrieveCompanyInfo:
    def __init__(self, pinecone_api_key: str, index_name: str, pdf_path: str):
        # Initialize Pinecone connection and the PDF document loader
        pinecone.init(api_key=pinecone_api_key, environment='us-west1-gcp')  
        self.index_name = index_name
        
        # Load and split the PDF
        loader = PyPDFLoader(pdf_path)
        documents = loader.load_and_split()
        
        # Initialize embeddings model and Pinecone index
        embeddings = OpenAIEmbeddings()
        self.vectorstore = Pinecone.from_documents(documents, embeddings, index_name=index_name)
    
    def retrieve_relevant_info(self, user_input: str) -> str:
        """
        This function retrieves relevant company information based on user input using Pinecone and embedding similarity.
        """
        # Perform a similarity search on Pinecone
        results = self.vectorstore.similarity_search(user_input, k=3)
        
        # Return the top matching documents as a string
        relevant_info = "\n".join([result['text'] for result in results])
        return relevant_info


# Chain 2
# Goal: Present information to the user
# Implementation: This chain receives both inputs (user input and most relevant mission and values) and generates a final output using a prompt template.
class PresentCompanyInfo:
    def __init__(self, prompt_template: str):
        self.prompt_template = prompt_template

    def format_company_info(self, user_input: str, retrieved_info: str) -> str:
        """
        Formats the retrieved company information into a user-friendly output using the given template.
        """
        # Create the final response
        formatted_response = self.prompt_template.format(user_input=user_input, company_info=retrieved_info)
        return formatted_response
