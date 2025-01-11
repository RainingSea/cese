import os

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self) -> dict:
        """Load users from the users.txt file."""
        users = {}
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        except FileNotFoundError:
            pass
        return users

    def save_users(self) -> None:
        """Save users to the users.txt file."""
        with open('users.txt', 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")

    def add_user(self, username: str, password: str) -> None:
        """Add a new user and save to the file."""
        self.users[username] = password
        self.save_users()

    def validate_user(self, username: str, password: str) -> bool:
        """Validate user credentials."""
        return self.users.get(username) == password

    def verify_user_data(self) -> bool:
        """Verify if user data is correctly saved."""
        for username, password in self.users.items():
            if not self.validate_user(username, password):
                return False
        return True