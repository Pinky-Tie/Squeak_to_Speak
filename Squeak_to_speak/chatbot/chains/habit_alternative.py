# User Story: I want to share details about a habit I wish to change to receive practical and quick suggestions with healthier alternatives.

# Chain 1
# Goal: Use RAG to retrieve an appropriate routine alternative
# Implementation: This Chain queries an embedding database (Pinecone) for relevant routines. Retrieved routines are ranked for relevance and utility.


# Chain 2
# Goal: Output response
# Implementation: This chain receives both inputs (user input and most relevant documents) and generates a final output using a prompt template.
