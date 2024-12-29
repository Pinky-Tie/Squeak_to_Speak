import sqlite3
from datetime import datetime

class UserDatabase:
    """
    Class to interact with SQLite database table 'Users'.
    
    Schema:
    - user_id: INTEGER PRIMARY KEY AUTOINCREMENT
    - username: TEXT NOT NULL
    - password: TEXT NOT NULL
    - email: TEXT UNIQUE NOT NULL
    - country: TEXT

    Methods provide operations for managing users.
    """
    def __init__(self, conn):
        self.conn = conn

    def add_user(self, username, password, email, country):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Users (username, password, email, country)
                VALUES (:username, :password, :email, :country)
                """,
                {"username": username, "password": password, "email": email, "country": country},
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
        finally:
            cursor.close()

    def get_user_details(self, user_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM Users WHERE user_id = :user_id", {"user_id": user_id})
            return cursor.fetchone()
        finally:
            cursor.close()

class TherapistDatabase:
    """
    Class to interact with the 'Therapists' table.

    Schema:
    - info_id: INTEGER PRIMARY KEY
    - TYPE: TEXT
    - name: TEXT
    - country: TEXT
    - email: TEXT
    - website: TEXT
    - phone: TEXT
    - Organization: TEXT
    - always_open: BOOLEAN
    - location: TEXT
    - avg_consult_price: INTEGER
    - specialty: TEXT
    - online_option: BOOLEAN
    - in_person_option: BOOLEAN

    Methods provide operations to query therapists.
    """
    def __init__(self, conn):
        self.conn = conn

    def get_therapists_by_preferences(self, country, specialty, max_price, online_option=None):
        cursor = self.conn.cursor()
        try:
            query = """
                SELECT * FROM Therapists
                WHERE country = :country AND specialty = :specialty AND avg_consult_price <= :max_price
            """
            params = {"country": country, "specialty": specialty, "max_price": max_price}
            if online_option is not None:
                query += " AND online_option = :online_option"
                params["online_option"] = online_option

            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()

class SupportGroupDatabase:
    """
    Class to interact with the 'Support_groups' table.

    Schema:
    - info_id: INTEGER PRIMARY KEY
    - TYPE: TEXT
    - name: TEXT
    - country: TEXT
    - email: TEXT
    - website: TEXT
    - phone: TEXT
    - Organization: TEXT
    - session_price: INTEGER
    - target_audience: TEXT
    - location: TEXT

    Methods provide operations to query support groups.
    """
    def __init__(self, conn):
        self.conn = conn

    def get_support_groups_by_preferences(self, country, target_audience, max_price):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                """
                SELECT * FROM Support_groups
                WHERE country = :country AND target_audience = :target_audience AND session_price <= :max_price
                """,
                {"country": country, "target_audience": target_audience, "max_price": max_price},
            )
            return cursor.fetchall()
        finally:
            cursor.close()

class GratitudeDatabase:
    """
    Class to interact with the 'Gratitude_entries' table.

    Schema:
    - id: INTEGER PRIMARY KEY
    - date: DATETIME
    - comment: TEXT

    Methods allow inserting gratitude messages.
    """
    def __init__(self, conn):
        self.conn = conn

    def add_gratitude_entry(self, comment):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Gratitude_entries (date, comment)
                VALUES (:date, :comment)
                """,
                {"date": datetime.now(), "comment": comment},
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding gratitude entry: {e}")
            return False
        finally:
            cursor.close()

class JournalDatabase:
    """
    Class to interact with the 'Journal' table.

    Schema:
    - message_id: INTEGER PRIMARY KEY
    - user_id: INTEGER
    - message: TEXT
    - date: DATETIME
    - hide_yn: BOOLEAN
    - time: DATETIME

    Methods allow creating and retrieving journal entries.
    """
    def __init__(self, conn):
        self.conn = conn

    def add_journal_entry(self, user_id, message, hide_yn):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Journal (user_id, message, date, hide_yn, time)
                VALUES (:user_id, :message, :date, :hide_yn, :time)
                """,
                {
                    "user_id": user_id,
                    "message": message,
                    "date": datetime.now(),
                    "hide_yn": hide_yn,
                    "time": datetime.now().time(),
                },
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding journal entry: {e}")
            return False
        finally:
            cursor.close()

    def get_journal_entries(self, user_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "SELECT * FROM Journal WHERE user_id = :user_id ORDER BY date DESC",
                {"user_id": user_id},
            )
            return cursor.fetchall()
        finally:
            cursor.close()

# Example usage:
# conn = sqlite3.connect("database.db")
# user_db = UserDatabase(conn)
# user_db.add_user("johndoe", "hashedpassword", "johndoe@example.com", "USA")
