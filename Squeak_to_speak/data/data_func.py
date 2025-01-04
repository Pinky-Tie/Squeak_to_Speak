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
    base_dir = Path(__file__).parent  
    db_path = base_dir / "database" / "squeaktospeak_db.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor

def retrieve_data():
    """
    Retrieve all user data from the users table in the database.

    Returns:
        dict: A dictionary where each key is a column name and values are lists of column data.
    """
    conn, cursor=connect_database()

    # Retrieve all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Assuming you know the table name, for example, 'users'
    table_name = "users"  # Replace this with your actual table name

    # Retrieve column names
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = [col[1] for col in cursor.fetchall()]

    # Retrieve data from the table
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Create a dictionary for each column
    column_data = {col: [] for col in columns}
    for row in rows:
        for idx, value in enumerate(row):
            column_data[columns[idx]].append(value)
    
    conn.close()
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
    conn, cursor=connect_database()
    cursor.execute(
        "INSERT INTO users (username, email, password, country) VALUES (?, ?, ?, ?)",
        (username, email, password, country)
    )
    conn.commit()
    conn.close()
    return True


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

    # Step 1: Get the user_id for the given email
    cursor.execute("SELECT user_id FROM users WHERE email = ?;", (email,))
    user_id_row = cursor.fetchone()

    if not user_id_row:
        print("No user found with the given email.")
        conn.close()
        return False

    user_id = user_id_row[0]

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
    FROM gratitude
    ORDER BY RANDOM()
    LIMIT ?;
    """
    cursor.execute(query, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows] 

