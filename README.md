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

#### 1. I want a recommendation for a healthcare professional

**Test Messages:**

1. "Can you recommend a therapist who specializes in anxiety and is based in Lisbon?"
2. "I'm looking for a therapist who can help with both depression and marriage issues. Can you find one?"
3. "I need a healthcare professional who can help me with bipolar disorder. Does the recommendation include online options?"

**Expected Behavior:**  
The chatbot should provide a personalized recommendation for a healthcare professional that fits the user’s specified needs and location, including any relevant options such as online services.

---

#### 2. I want to know about support groups in my area

**Test Messages:**

1. "Are there any support groups for people struggling with anxiety in Lisbon?"
2. "Can you tell me if there are any grief support groups near me?"
3. "I need a support group for people who have dealt with childhood trauma. Do you have anything like that?"

**Expected Behavior:**  
The chatbot should provide information about local support groups that match the user's needs, including details like group type and location.

---

#### 3. I want a contact for an emergency or non-emergency hotline

**Test Messages:**

1. "What’s the contact for a suicide prevention hotline in my area?"
2. "I need the contact for a mental health crisis hotline in Lisbon, please."
3. "Can you provide the contact for a non-emergency mental health helpline that operates after hours?"

**Expected Behavior:**  
The chatbot should provide the appropriate hotline contact information based on the urgency and location specified by the user.

---

#### 4. I want an alternative to a habit I have

**Test Messages:**

1. "I’ve been eating junk food late at night. Can you suggest a healthier alternative?"
2. "I want to stop smoking. What can I do instead to cope with stress?"
3. "I need help with an unhealthy habit where I overwork myself. How can I balance work and relaxation better?"

**Expected Behavior:**  
The chatbot should offer practical and healthy alternatives to the user's habits, tailored to the specifics of their request.

---

#### 5. I want to make an entry in my journal or mood board

**Test Messages:**

1. "Can you add an entry in my journal saying that I'm feeling overwhelmed today?"
2. "Can you add a mood board entry with a quote I liked today?"
3. "I want to write about my anxiety, but I don’t know how to express it. Can you help me get started?"

**Expected Behavior:**  
The chatbot should add a new entry to the user's journal or mood board based on their input and ensure it is saved for future reference.

---

#### 6. I want to see my journal or mood board

**Test Messages:**

1. "Can you show me what I wrote in my journal last week?"
2. "Can I look at all my entries about stress from the past month?"
3. "I forgot if I wrote anything positive in my mood board last week. Can you check?"

**Expected Behavior:**  
The chatbot should retrieve and display relevant entries from the user's journal or mood board, allowing them to review their past thoughts and emotions.

---

#### 7. I want to make an entry on the community gratitude banner

**Test Messages:**

1. "I want to share that I’m grateful for my family. Can you add that to the gratitude banner?"
2. "I want to share something really personal that I'm thankful for. Can it remain anonymous?"
3. "Can I add an entry about how grateful I am for this service?"

**Expected Behavior:**  
The chatbot should add an entry to the community gratitude banner, ensuring it respects any privacy preferences.

---

#### 8. I want to know more about Squeak to Speak mission and values

**Test Messages:**

1. "Can you tell me more about what Squeak to Speak stands for?"
2. "How does Squeak to Speak incorporate mental health awareness into its mission?"
3. "What values drive the development of Squeak to Speak’s AI assistant?"

**Expected Behavior:**  
The chatbot should provide clear information about the company's mission, values, and how they align with its services and technology.

---

#### 9. I want to know what Squeak and Speak can do for me

**Test Messages:**

1. "What features does Squeak to Speak offer for managing mental health?"
2. "Can I use Squeak to Speak to find mental health professionals and attend support groups?"
3. "What can Squeak to Speak do to help me with stress and anxiety management?"

**Expected Behavior:**  
The chatbot should outline the key features and capabilities of Squeak to Speak, helping the user understand how it can assist them with their mental health.

---

#### 10. I want to know what Squeak and Speak knows about me

**Test Messages:**

1. "Can you tell me what information Squeak to Speak holds about my mental health?"
2. "What kind of data does Squeak to Speak keep about my journal entries and mood board?"
3. "I want to know if Squeak to Speak tracks any personal information, like my preferences or location."

**Expected Behavior:**  
The chatbot should provide transparency about the data Squeak to Speak collects, how it's used, and what the user can review or modify.

---

#### 11. I want to delete data from my Journal or Mood Board

**Test Messages:**

1. "Can you delete the last entry from my journal?"
2. "I want to delete an entire month of entries from my mood board. Can you do that?"
3. "Can you permanently remove all my journal entries from the past year?"

**Expected Behavior:**  
The chatbot should delete the requested data from the journal or mood board and confirm the deletion.

---

#### 12. I want to alter data on my Journal or Mood Board

**Test Messages:**

1. "Can you update my journal entry from yesterday to reflect how I feel now?"
2. "I want to edit my mood board entry to add that I’m feeling more positive."
3. "Can you change the date on my journal entry from last week to today’s date?"

**Expected Behavior:**  
The chatbot should allow the user to modify existing entries with new information, ensuring the updates are correctly saved.

---

#### 13. I want to talk to the Chatbot having the knowledge of what I wrote in my journal

**Test Messages:**

1. "Can you help me reflect on my journal entries about stress?"
2. "Can you remember what I wrote last month about feeling overwhelmed?"
3. "Can you pull up some of my past journal entries on mental health challenges so we can talk about them?"

**Expected Behavior:**  
The chatbot should recall relevant journal or mood board entries and use that knowledge to provide personalized and empathetic responses.




## 5. Intention Router

### 5.1 Intention Router Implementation

- **Message Generation**:  
  Describe how you generated messages for each user intention. Did you create the messages manually, use synthetic data, or leverage a dataset? Specify the method used and tools/scripts for generating the data.  
  Where are the generated messages stored (e.g., in a file, database, or another format)?

### 5.2 Semantic Router Training

- **Hyperparameters**:  
  Report which encoder was used in the semantic router.  
  Report the aggregation method and the `top_k` parameter used for selecting the most relevant results.

### 5.3 Post-Processing for Accuracy Improvement

- **Post-Processing Techniques**:  
  If you applied any post-processing techniques to enhance the router's accuracy, describe them here.  
  For example, did you use a Large Language Model (LLM) for additional refinement?  
  Explain how these techniques were integrated into the pipeline and any custom code or algorithms used.

---

## 6. Intention Router Accuracy Testing Results

### Methodology

1. **Message Creation**:

   - Generate at least 50 messages per intention, totaling 400 messages. These can be either synthetic or human-generated.
   - Additionally, generate at least 25 small-talk messages related to your company and 25 off-topic messages unrelated to the company, labeled as "None."

2. **Data Splitting**:

   - Split the dataset into training and testing sets (90/10), ensuring a balanced distribution of each intention across both sets.

3. **Training the Semantic Router**:

   - Use the training split to train the semantic router. Report the accuracy on both the training and testing splits.

4. **Post-Processing with LLM**:

   - If applicable, apply post-processing using an LLM to improve the accuracy of the router. Report accuracy on both the training and testing splits after post-processing.

5. **Reporting Results**:
   - Report the accuracy for each intention, as well as the overall accuracy. Accuracy should be calculated as the percentage of correct responses out of the total inputs for each intention.

### Results

Present the accuracy results in a table format:

| Intention            | Test Inputs | Correct | Incorrect | Accuracy (%) |
| -------------------- | ----------- | ------- | --------- | ------------ |
| Product Information  | 10          | 9       | 1         | 90%          |
| Order Status         | 10          | 8       | 2         | 80%          |
| Create Order         | 10          | 7       | 3         | 70%          |
| **Average Accuracy** | 30          | 24      | 6         | 80%          |

```

```
