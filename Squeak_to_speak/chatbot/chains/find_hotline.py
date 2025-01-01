# User Story: I want the chatbot to provide contact information for relevant hotlines to quickly access support during emergencies or non-urgent situations.

# Chain 1
# Goal: Identify user’s preferences for a hotline
# Implementation: This chain retrieves relevant data from the user input and all relevant information from the database. Creating a Pydantic model instance containing all information. At the end, the chain returns the information in a string format.


# Chain 2
# Goal: Identify the best hotline
# Implementation: This chain processes the user preferences generated by the previous chain, queries the database for the most relevant entries, and retrieves the best matches.


# Chain 3
# Goal: Output the best support group
# Implementation: This chain receives both inputs (user input and best hotline match) and generates a final output using a prompt template.
