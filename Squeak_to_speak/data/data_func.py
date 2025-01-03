import sqlite3
from pathlib import Path

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