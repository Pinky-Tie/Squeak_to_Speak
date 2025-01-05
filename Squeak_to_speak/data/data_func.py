import sqlite3
from pathlib import Path
from datetime import datetime
import random

# Connect to the SQLite database
def connect_database():
    """
    Connect to the SQLite database 
    
    Returns:
        The connection and cursor.
    """
    db_file = r"C:\Users\pedro\Downloads\Squeak_to_Speak\Squeak_to_speak\data\Squeaktospeak_db.db"

    conn_1 = sqlite3.connect(db_file)
    cursor_1 = conn_1.cursor()
    return conn_1, cursor_1

def retrieve_data():
    """
    Retrieve all user data from the users table in the database.

    Returns:
        dict: A dictionary where each key is a column name and values are lists of column data.
    """
    conn_2, cursor_2=connect_database()

    # Retrieve all table names
    cursor_2.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor_2.fetchall()

    table_name = "users"  

    # Retrieve column names
    cursor_2.execute(f"PRAGMA table_info({table_name});")
    columns = [col[1] for col in cursor_2.fetchall()]

    # Retrieve data from the table
    cursor_2.execute(f"SELECT * FROM {table_name}")
    rows = cursor_2.fetchall()

    # Create a dictionary for each column
    column_data = {col: [] for col in columns}
    for row in rows:
        for idx, value in enumerate(row):
            column_data[columns[idx]].append(value)
    
    conn_2.close()
    return column_data

def is_email_unique(email):
    """
    Check if the given username is unique in the user data dictionary.

    Args:
        username (str): The username to check.
        user_data (dict): Dictionary containing user information.

    Returns:
        bool: True if the username is unique, False otherwise.
    """
    user_data=retrieve_data()
    return email not in user_data["username"]

def add_user(username, email, password, country):
    """
    Add a new user to the database.

    Args:
        username (str): The username of the new user.
        email (str): The email address of the new user.
        password (str): The hashed password of the new user.
        country (str): The country of the new user.

    Returns:
        bool: True if the user was added successfully, False otherwise.
    """
    conn, cursor = connect_database()

    # Get the maximum user_id currently in the table
    cursor.execute("SELECT MAX(user_id) FROM users")
    max_user_id = cursor.fetchone()[0]

    # If there are no users, start with user_id = 1
    new_user_id = (max_user_id or 0) + 1

    # Insert the new user with the calculated user_id
    cursor.execute(
        "INSERT INTO users (user_id, username, email, password, country) VALUES (?, ?, ?, ?, ?)",
        (new_user_id, username, email, password, country)
    )

    conn.commit()
    conn.close()
    return True



def get_user_id(email):
    """
    Get the user ID for a given email address.

    Args:
        email (str): The email address of the user.

    Returns:
        int: The user ID if the email is found, None otherwise.
    """
    conn, cursor=connect_database()
    cursor.execute("SELECT user_id FROM users WHERE email = ?;", (email,))
    user_id_row = cursor.fetchone()
    conn.close()
    return user_id_row[0] if user_id_row else None

def get_jornal_entries(email, target_date=None):
    """
    Fetch jounrnal entry for a user based on their email and a specific date.

    Args:
        email: The email of the user.
        target_date: The date to filter entries (default is today in 'YYYY-MM-DD' format).

    Returns:
        List of strings if entries exist, or False if no entries are found.
    """
    conn, cursor = connect_database()

    # Use today's date if no specific date is provided
    if not target_date:
        target_date = datetime.now().strftime("%Y-%m-%d")

   

    user_id = get_user_id(email)

    # Step 2: Get mood and description for the given user_id and date
    query = """
    SELECT message 
    FROM journal 
    WHERE user_id = ? AND date(date) = ?;
    """
    cursor.execute(query, (user_id, target_date))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return False  # No records for the given date

    return rows



def gratitude_comments(limit=5):
    """
    Fetch a specified number of random comments from the Gratitude_entries table.

    Args:
        conn: SQLite database connection object.
        limit: The number of random rows to fetch (default is 4).

    Returns:
        A list of comments if available, otherwise an empty list.
    """
    conn, cursor = connect_database()

    # Query to fetch random rows
    query = f"""
    SELECT comment
    FROM Gratitude_entries
    ORDER BY RANDOM()
    LIMIT ?;
    """
    cursor.execute(query, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows] 




# Connect to the database
conn, cursor = connect_database()

# Query to get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()  # Fetch all table names

# Print table names
table_names = [table[0] for table in tables]  # Extract table names from tuples
print("Tables in the database:", table_names)

# Iterate over each table and fetch one row
for table in tables:
    table_name = table[0]
    print(f"Table: {table_name}")
    try:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 1;")
        row = cursor.fetchone()  # Fetch one row
        if row:
            print(f"Sample row: {row}")
        else:
            print("Table is empty.")
    except sqlite3.OperationalError as e:
        print(f"Could not query table {table_name}. Error: {e}")

# Close the connection
conn.close()