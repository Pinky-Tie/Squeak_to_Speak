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

# Basic Insert Operations
## User Registration
class UserManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_user(self, username, password, email, country):
        """
        Validates and adds a new user to the database.

        Args:
            username (str): The user's username.
            password (str): The user's password (hashed).
            email (str): The user's email.
            country (str): The user's country.

        Returns:
            str: Success or failure message.
        """
        # Basic validation
        if not username or not email or not password or not country:
            return "All fields are required."

        if self.db_manager.check_if_email_exists(email):
            return "This email is already registered."

        data = {
            "username": username,
            "password": password,
            "email": email,
            "country": country
        }

        # Attempt to insert the new user into the database
        success = self.db_manager.insert("Users", data)

        if success:
            return "User has been registered successfully!"
        else:
            return "An error occurred while registering. Please try again."

## Insert Journal entry
class JournalManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_entry(self, user_id, message, date, hide_yn, time):
        data = {
            "user_id": user_id,
            "message": message,
            "date": date,
            "hide_yn": hide_yn,
            "time": time,
        }
        return self.db_manager.insert("Journal", data)

class JournalEntryResponse:
    def generate_response(self, success):
        return "Entry added successfully." if success else "Failed to add your entry."

## Insert Gratitude message
class GratitudeManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_gratitude_message(self, comment):
        # Validates and adds a gratitude message to the database.
        if not comment or len(comment.strip()) == 0:
            return "Your gratitude message cannot be empty."

        data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "comment": comment,
        }

        # Attempt to insert the gratitude message into the database
        success = self.db_manager.insert("Gratitude_entries", data)

        if success:
            return "Your gratitude message has been added successfully!"
        else:
            return "An error occurred. Please try again."



# Feature-specific Database Classes

## Use 1: I want a recommendation for a therapist
### Chain 1: Get User preferences
class UserPreferencesModel(BaseModel):
    mental_health_needs: str
    location: str
    budget: int = None
    online_option: bool = None

class IdentifyUserPreferences:
    def process_input(self, user_input: dict):
        try:
            preferences = UserPreferencesModel(**user_input)
            return preferences
        except ValidationError as e:
            return {"error": str(e)}

### Chain 2: Get a Therapist match
class TherapistFinder:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def find_best_match(self, preferences):
        query = """
        SELECT * FROM Therapists
        WHERE country = :location
          AND specialty LIKE :mental_health_needs
          AND (avg_consult_price <= :budget OR :budget IS NULL)
          AND (online_option = :online_option OR :online_option IS NULL)
        ORDER BY avg_consult_price ASC
        LIMIT 1
        """
        params = {
            "location": preferences.location,
            "mental_health_needs": f"%{preferences.mental_health_needs}%",
            "budget": preferences.budget,
            "online_option": preferences.online_option,
        }
        results = self.db_manager.select(query, params)
        return results

### Chain 3: Output the best therapist
class TherapistOutputFormatter:
    def format_output(self, therapist, user_input):
        if therapist:
            return (
                f"Based on your needs for {user_input['mental_health_needs']}, "
                f"we recommend {therapist[0]['name']} located in {therapist[0]['location']}. "
                f"They charge an average of {therapist[0]['avg_consult_price']}."
            )
        return "No suitable therapist found for your preferences."


## Use 2: I want to know about support groups in my area
