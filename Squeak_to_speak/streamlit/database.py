
import re

users_dict= {
    "usernames": {
        "maria@example.com": {
            "name": "Maria",
            "password": "123"
        },
        "user@example.com": {
            "name": "User",
            "password": "123456"
        }
    }
}


def email_unique(username):
    return username not in users_dict["usernames"]
    
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None   

def add_user(name, username, password, country):
    users_dict["usernames"][username] = {
        "name": name,
        "password": password,
        "country": country
    }
    return True