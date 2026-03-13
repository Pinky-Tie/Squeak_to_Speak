  # Squeak To Speak

  ## 1. Project Overview

  - **Company Name**: Squeak to Speak - DEMO VERSION
  ---

  ### 2.1 Prerequisites

  - **Python Version**: 3.10.11
  - **Dependencies**:  
    Found also in requirements.txt
    
    - langchain v.0.3.9
    - langchain-openai v.0.2.10
    - openai v.1.55.3
    - pandas v.2.2.3
    - pydantic v.2.10.2
    - python-dotenv v.1.0.1
    - streamlit v.1.40.2
    - torch v.2.5.1
    - transformers v.4.46.3
    - langchain-pinecone v.0.2.0
    - pinecone-client v.5.0.1
    - semantic-router v.0.0.72
    - langchain-community v.0.3.4
    - python-dotenv v.1.0.1

  - **Environment Setup**:
To set up your environment for testing the chatbot, follow these steps:

  *Option 1: Using venv (virtual environment)*
  1. Create a virtual environment:
      python3 -m venv squeak-to-speak-env

  2. Activate the virtual environment:
     
    - On Windows:
      squeak-to-speak-env\Scripts\activate

    - On macOS/Linux:
      source squeak-to-speak-env/bin/activate

  3. Install dependencies: Ensure that requirements.txt is available in the root of your repository and install the necessary packages by running:
  
    pip install -r requirements.txt


  *Option 2: Using Conda Environment*
  1. Create a conda environment:
     
    conda create --name squeak-to-speak python=3.10.11

  3. Activate the environment:

    conda activate squeak-to-speak
  
  5. Install dependencies:

    pip install -r requirements.txt

  An In console version of the chatbot can be run with **console_app.py**


### 2.2 How to Run the Chatbot

Once the environment is set up, you can run the chatbot locally as explained below.

1. Run the Streamlit app by typing in the terminal:

    streamlit run app.py

The app will start, and you can open your browser to http://localhost:8501 to interact with the Squeak to Speak chatbot.

2. Log in to the platform, by browsing to the Login page. 
The user account for testing is the following:
*carlos.rossi33@example.com * - *byBjmFAT *

