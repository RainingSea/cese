import os

class UserManager:
    """Manages user registration and authentication."""
    
    def __init__(self, filename: str):
        """Initializes UserManager with a given filename."""
        self.filename = filename
        self.users = self.load_users()

    def load_users(self) -> dict:
        """Loads users from a file into a dictionary."""
        users = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        return users

    def register(self, username: str, password: str) -> bool:
        """Registers a new user if the username is not already taken."""
        if username in self.users:
            return False  # User already exists

        self.users[username] = password
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True  # Registration successful

    def login(self, username: str, password: str) -> bool:
        """Validates user login credentials."""
        return self.users.get(username) == password

    def get_users(self) -> list:
        """Returns a list of registered usernames."""
        return list(self.users.keys())