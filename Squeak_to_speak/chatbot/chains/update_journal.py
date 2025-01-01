# User Story: I want to modify entries in my journal to correct errors and make necessary updates.

# Chain 1
# Goal: Identify which entry the user wants to modify
# Implementation: This chain identifies the query the user wishes to alter and outputs it as an object.


# Chain 2
# Goal: Alter the entry with the users' inputs
# Implementation: This chain takes as input the entry to be altered and the user input, structures the new values for the entry and alters it, outputting confirmation for the alteration.


# Chain 3
# Goal: Inform the user that the entry has been changed
# Implementation: This chain receives both inputs (user input and alteration confirmation) and generates a final output using a prompt template.