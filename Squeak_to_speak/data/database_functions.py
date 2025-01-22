# General Database Classes
import sqlite3
from pydantic import BaseModel, ValidationError
import datetime

class DatabaseManager:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, table: str, data: dict) -> dict:
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?'] * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            self.conn.execute(query, tuple(data.values()))
            self.conn.commit()
            return {"success": True}
        except Exception as e:
            print(f"Error inserting into {table}: {e}")
            return {"success": False, "error": str(e)}

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
