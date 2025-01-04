# General Database Classes
import sqlite3
from pydantic import BaseModel, ValidationError
import datetime

class DatabaseManager:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, table_name, data):
        placeholders = ", ".join(f":{key}" for key in data.keys())
        columns = ", ".join(data.keys())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, data)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error inserting into {table_name}: {e}")
            return False
        finally:
            cursor.close()

    def select(self, query, params=None):
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params or {})
            return cursor.fetchall()
        finally:
            cursor.close()

    def update(self, query, params=None):
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params or {})
            self.conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()

    def delete(self, query, params=None):
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params or {})
            self.conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()

    def check_if_email_exists(self, email):
        # Check if an email already exists in the database.
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "SELECT email FROM Users WHERE email = :email", {"email": email}
            )
            return cursor.fetchone() is not None
        finally:
            cursor.close()
