  # Squeak To Speak

  ## 1. Project Overview

  - **Company Name**: Squeak to Speak
  - **Group 11**: Joana Sanches, Margarida Sardinha, Margarida Marchão, Maria Santos, Renato Bernardino
  - **Description**:  
    Squeak to Speak revolutionizes access to mental health resources through conversational AI that provides personalized and context-based recommendations. By including LLM technology, the AI assistant continuously adapts to user needs and preferences, creating a personalized and adaptable support path that encourages emotional growth and helps users connect with the most suitable mental health resources. This approach ensures a comfortable journey toward emotional well-being, making it easier for users to find the right support while also ensuring the effective use of human psychological resources.
  ---

  ## 2. How to Test the Chatbot

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
*username* - *password*



## 3. Database Schema

### 3.1 Database Overview and Schema Diagram
This is the database operating behind the chatbot.

![Database Schema](database_schema.png "Database Schema")

### 3.2 Table Descriptions

__Users Table__ :
General info on each of the users. Required for sign in and basic operations.

- user_id: Numeric (Primary Key) - Unique identifier for a user. 
- username: Varchar(30) - The username of the user.
- password: Varchar(50) - The user's password.
- email: Nvarchar(50) - The user's email address.
- country: Nvarchar(30) - The user's country.

__Mood_tracker Table__ :
Mood tracker entries made by the users. Each entry corresponds to the daily mood of the user

- mood_id: Numeric (Primary Key) - Unique identifier for each mood tracking entry.
- user_id: Numeric (Foreign Key) - Reference to the user who created the entry.
- mood: Nvarchar(20) - The recorded mood 
- date: Datetime - Date of the mood entry.
- description: Text - Additional details or description of the mood.

__Journal Table__ :
Journal entries made by the users. Being "hiden" means that the message will not be used by the chatbot unless told so

- message_id: Numeric (Primary Key) - Unique identifier for each journal entry.
- user_id: Numeric (Foreign Key) - Reference to the user who wrote the journal entry.
- message: Text - Content of the journal entry.
- date: Datetime - Date of the journal entry.
- hide_yn: Bit - Indicates whether the journal entry is hidden (Boolean).
- time: Datetime - Time of the journal entry.
  
__Gratitude_entries Table__ :
Gratitude quotes written by the users, to be shown in a rolling banner to all users.

- id: Numeric (Primary Key) - Unique identifier for each gratitude entry.
- date: Datetime - Date of the gratitude entry.
- comment: Nvarchar(200) - Content of the gratitude entry.

__Helpful_Info Table__:
Mother table to the various types of information the chatbot may give out. Subdivides into Help_lines, Therapists and Support_groups

- Info_id: Numeric (Primary Key) - Unique identifier for helpful information entries.
- TYPE: Nvarchar(255) - Type of information (e.g., helpline, therapist, support group).
- name: Nvarchar(100) - Name of the resource.
- country: Nvarchar(30) - Country of the resource.
- email: Nvarchar(50) - Email address of the resource.
- website: Nvarchar(80) - Website of the resource.
- phone: Nvarchar(12) - Phone number of the resource.
- Organization: Nvarchar(255) - Name of the associated organization.

__Help_lines Table (Subtype of Helpful_Info)__
- always_open: Bit - Indicates if the helpline operates 24/7 (Boolean).
- specialty: Nvarchar(100) - Focus or specialty of the helpline (e.g., mental health, crisis).

__Therapists Table (Subtype of Helpful_Info)__
- always_open: Bit - Indicates if the therapist provides 24/7 services (Boolean).
- location: Nvarchar(80) - Location of the therapist's office.
- avg_consult_price: Smallint - Average consultation price of the therapist.
- specialty: Nvarchar(100) - Focus or specialty of the therapist (e.g., CBT, trauma).
- online_option: Bit - Indicates if online consultations are available (Boolean).
- in_person_option: Bit - Indicates if in-person consultations are available (Boolean).

__Support_groups Table (Subtype of Helpful_Info)__
- session_price: Smallint - Price of group sessions.
- target_audience: Nvarchar(100) - Intended audience of the support group (e.g., teens, veterans).
- location: Nvarchar(80) - Location of the support group sessions.


## 4. User Intentions

### 4.1 Implemented Intentions

**1: I want a recommendation for a healthcare professional**

Using details about the user's mental health needs, preferences, and location, deliver a personalized recommendation for a healthcare professional who matches their needs and preferences.

**2: I want to know about support groups in my area**

Recommend support groups to both inform the user about the support available and also to help them connect with people who face similar problems.

**3: I want a contact for an emergency or non-emergency hotline**

Provide contact information for relevant hotlines to quickly access support during emergencies or non-urgent situations.

**4: I want an alternative to a habit I have**

Using details about a habit the user wishes to change, deliver practical and quick suggestions with healthier alternatives.

**5: I want to make an entry in my journal or mood board**

Document the user's thoughts and feelings in a private journal or mood board to reflect, vent or track their mental health journey in a safe space.

**6: I want to see my journal or mood board**

Allows the user to revisit past entries in their journal or mood board to reflect, recall and understand their experiences and emotions over time

**7: I want to make an entry on the community gratitude banner**

Allows the user to anonymously share something they're grateful and/or happy for so that they can help brighten someone else’s day while fostering their own positivity.

**8: I want to know more about Squeak to Speak mission and values**

Allows the user to learn more about Squeak to Speak as a company to build trust and confidence in its services.

**9: I want to know what Squeak and Speak can do for me**

Allows the user to explore Squeak to Speak’s features to make the most of its capabilities.

**10: I want to know what Squeak and Speak knows about me**

Review the data Squeak to Speak holds about the user to better understand what is collected and how it is used.

**11: I want to delete data from my Journal or Mood Board**

Delete entries from the user's journal or mood board to maintain control over the information stored about them.

**12: I want to alter data on my Journal or Mood Board**

Modify entries in the user's journal or mood board to correct errors and make necessary updates.

**13: I want to talk to the Chatbot having the knowledge of what I wrote in my journal**

Communicate with Squeak to Speak’s assistant, leveraging its understanding of the user's journal and mood board to create more empathetic interactions.


### 4.2 How to Test Each Intention

For each intention, provide 3 examples of test messages that users can use to verify the chatbot's functionality. Include both typical and edge-case inputs to ensure the chatbot handles various scenarios.

#### 1. Review User Memory

**Test Messages:**
1. "What information is stored about my interactions?"
2. "What insights do you have on my preferences?"
3. "What data is stored regarding my journal entries?"

**Expected Behavior:**  
The chatbot should provide a summary of stored data, ensuring transparency and clarity about user-specific information.

---

#### 2. Find Therapist

**Test Messages:**
1. "Help me find a therapist that focuses on trauma and offers online sessions."
2. "Help me find a therapist that is LGBTQ+ friendly and has evening availability."
3. "Help me find a therapist that specializes in anxiety and is affordable."

**Expected Behavior:**  
The chatbot should recommend therapists based on user-specified preferences such as specialization, availability, and budget.

---

#### 3. Find Support Group

**Test Messages:**
1. "Help me find a support group that focuses on anxiety in New York."
2. "Help me find a support group that offers in-person meetings for loneliness."
3. "Help me find a support group that meets online for depression."

**Expected Behavior:**  
The chatbot should provide a list of relevant support groups based on the user's criteria.

---

#### 4. Find Hotline

**Test Messages:**
1. "Help me find a hotline that provides general counseling services."
2. "Help me find a hotline that offers immediate crisis support."
3. "Help me find a hotline that specializes in mental health issues."

**Expected Behavior:**  
The chatbot should suggest hotline numbers for various needs, including 24/7 services and specific areas of concern.

---

#### 5. Habit Alternatives

**Test Messages:**
1. "Suggest an alternative for snacking on chips."
2. "Suggest an alternative for procrastinating on my tasks."
3. "Suggest an alternative for skipping my workouts."

**Expected Behavior:**  
The chatbot should provide practical and healthier alternatives for the user's current habits.

---

#### 6. Insert Mood

**Test Messages:**
1. "Today, I feel excited about starting my new project."
2. "Today, I feel nostalgic thinking about my childhood."
3. "Today, I feel frustrated with the challenges I'm facing."

**Expected Behavior:**  
The chatbot should record the user's mood and store it on the mood board.

---

#### 7. Insert Journal

**Test Messages:**
1. "I want to add to my journal today: I felt really happy after my walk."
2. "I want to add to my journal today: I learned something new today that excited me."
3. "I want to add to my journal today: Today was a productive day at work."

**Expected Behavior:**  
The chatbot should save the journal entry accurately.

---

#### 8. Insert Gratitude

**Test Messages:**
1. "I am grateful for the laughter shared with my colleagues."
2. "I am grateful for the beautiful sunset I saw today."
3. "I am grateful for the opportunity to learn something new today."

**Expected Behavior:**  
The chatbot should append the gratitude message to the community gratitude banner.

---

#### 9. Ask Mission/Values

**Test Messages:**
1. "Tell me about Squeak to Speak's story and how it started."
2. "Tell me about Squeak to Speak's vision for the future."
3. "Tell me about Squeak to Speak and its core values."

**Expected Behavior:**  
The chatbot should provide details about the platform's mission, vision, and values.

---

#### 10. Ask Features

**Test Messages:**
1. "Tell me about your chatbot and its role in supporting mental health."
2. "Tell me about your chatbot's features and how they can aid my well-being."
3. "Tell me about your chatbot and the resources it provides for mental wellness."

**Expected Behavior:**  
The chatbot should summarize its key features and functionalities.

---

#### 11. Update Journal

**Test Messages:**
1. "I want to change a journal entry from 2023-10-05 to correct a mistake."
2. "I want to change a journal entry from 2023-10-01 to reflect my new feelings."
3. "I want to change a journal entry on 2023-07-30 to include my recent thoughts."

**Expected Behavior:**  
The chatbot should allow modifications to existing journal entries and ensure changes are saved.

---

#### 12. Update Mood

**Test Messages:**
1. "I want to change my mood on 2023-10-01 to reflect feeling more hopeful."
2. "I want to change my mood on 2023-10-12 to reflect that I'm feeling sad."
3. "I want to change my mood on 2023-08-25 to indicate I'm feeling motivated."

**Expected Behavior:**  
The chatbot should update the mood entry on the mood board with the new details.

---

#### 13. View Journal

**Test Messages:**
1. "How does my journal look from last month?"
2. "How does my journal look for the year?"
3. "What have I added to my journal entries?"

**Expected Behavior:**  
The chatbot should display the requested journal entries based on the user's timeframe or topic.

---

#### 14. View Mood

**Test Messages:**
1. "What does my mood board look like for this month?"
2. "How has my mood been on 2023-10-10?"
3. "What does my mood board look like for the past few days?"

**Expected Behavior:**  
The chatbot should show mood entries corresponding to the specified time period.

---

#### 15. Delete Journal

**Test Messages:**
1. "Delete my journal entry on 2023-01-22."
2. "Delete my journal entry on 2023-10-01."
3. "Delete my journal entry on 2023-08-20."

**Expected Behavior:**  
The chatbot should remove the specified journal entry.

---

#### 16. Delete Mood

**Test Messages:**
1. "Delete my mood on 2023-08-20."
2. "Delete my mood on 2023-03-12."
3. "Delete my mood on 2023-06-25."

**Expected Behavior:**  
The chatbot should delete the corresponding mood board entry.





## 5. Intention Router

### 5.1 Intention Router Implementation

- **Message Generation**:  
  Each message was artificially created with the use of the same OpenAI model used in the chatbot. The prompts and parameters can be found
  in generate_intentions.ipynb

### 5.2 Semantic Router Training

- **Hyperparameters**:  
  The HuggingFace Enconder was used to train the semantic router, mantaining the default agregation and top_k params.


## 6. Intention Router Accuracy Testing Results

### Methodology
    To accuractly train and test the intention router, the following steps were taken:

   - With the artificial method explained above,  generated 100 messages per intention and 25 messages with no intention.
   - Splitted the dataset into train and test subparts (80/20)
   - Trained the and evaluated the semantic router. Obtaining a test accuracy score of 71.79%



5. **Reporting Results**:

### Results


| Intention              | Test Inputs | Correct | Incorrect | Accuracy (%) |
|------------------------|-------------|---------|-----------|--------------|
| insert_journal         | 2           | 0       | 2         | 0.0          |
| delete_journal         | 4           | 4       | 0         | 100.0        |
| update_mood            | 1           | 1       | 0         | 100.0        |
| find_therapist         | 3           | 3       | 0         | 100.0        |
| view_journal           | 2           | 2       | 0         | 100.0        |
| update_journal         | 3           | 3       | 0         | 100.0        |
| ask_missionvalues      | 4           | 4       | 0         | 100.0        |
| None                   | 1           | 1       | 0         | 100.0        |
| delete_mood            | 3           | 3       | 0         | 100.0        |
| review_user_memory     | 3           | 0       | 3         | 0.0          |
| insert_gratitude       | 2           | 1       | 1         | 50.0         |
| view_mood              | 1           | 1       | 0         | 100.0        |
| ask_features           | 1           | 1       | 0         | 100.0        |
| habit_alternatives     | 2           | 0       | 2         | 0.0          |
| find_hotline           | 1           | 0       | 1         | 0.0          |
| **Average Accuracy**   | **33**      | **24**  | **9**     | **72.73**    |



```

```
