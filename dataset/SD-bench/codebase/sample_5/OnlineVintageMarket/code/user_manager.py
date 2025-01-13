from typing import List
from user import User

class UserManager:
    """Manage user data and operations."""
    
    def __init__(self):
        self.users: List[User] = []

    def load_users(self) -> None:
        """Load users from a file."""
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.add_user(username, password)
        except FileNotFoundError:
            pass

    def save_users(self) -> None:
        """Save users to a file."""
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}\n")

    def add_user(self, username: str, password: str) -> None:
        """Add a new user."""
        user = User(username, password)
        self.users.append(user)
        self.save_users()

    def find_user(self, username: str) -> User:
        """Find a user by username."""
        for user in self.users:
            if user.username == username:
                return user
        return None