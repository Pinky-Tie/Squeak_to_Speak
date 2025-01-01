# User Story: I want to learn more about Squeak to Speak as a company to build trust and confidence in its services.

# Chain 1
# Goal: Use RAG to retrieve information related to the users' input
# Implementation: This chain queries an embedding database (Pinecone) for relevant routines. Retrieved routines are ranked for relevance and utility.


# Chain 2
# Goal: Present information to the user
# Implementation: This chain receives both inputs (user input and most relevant mission and values) and generates a final output using a prompt template.
