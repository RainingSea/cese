import os

class User:
    """Represents a user with a username and password."""
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class UserManager:
    """Manages user registration and login functionality."""
    
    def __init__(self):
        self.users = self.load_users()

    def register(self, username: str, password: str) -> bool:
        """Registers a new user if the username is not already taken."""
        if username not in self.users:
            self.users[username] = password
            self.save_users()
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        """Logs in a user if the credentials are valid."""
        return self.users.get(username) == password

    def load_users(self) -> dict:
        """Loads users from a file into a dictionary."""
        if not os.path.exists('users.txt'):
            return {}
        with open('users.txt', 'r') as file:
            return dict(line.strip().split('|') for line in file)

    def save_users(self) -> None:
        """Saves the current users to a file."""
        with open('users.txt', 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")