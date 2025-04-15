import os

class UserManager:
    """Manages user registration and login."""
    users_file = 'users.txt'

    def __init__(self):
        """Initialize UserManager and load users from file."""
        self.users = self.load_users()

    def load_users(self) -> dict:
        """Load users from a file."""
        users_dict = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users_dict[username] = password
        return users_dict

    def register(self, username: str, password: str) -> bool:
        """Register a new user."""
        if username not in self.users:
            with open(self.users_file, 'a') as file:
                file.write(f"{username}|{password}\n")
            self.users[username] = password
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        """Login a user."""
        return self.users.get(username) == password

    def logout(self) -> None:
        """Logout a user."""
        # This function will be handled in the main application logic
        pass