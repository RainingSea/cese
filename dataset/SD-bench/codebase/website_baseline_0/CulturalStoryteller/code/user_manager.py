class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def register(self, username: str, password: str) -> bool:
        """Register a new user with the provided username and password."""
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        """Log in a user by checking the username and password."""
        return self.users.get(username) == password

    def load_users(self) -> dict:
        """Load users from a file into a dictionary."""
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
        """Save the current users to a file."""
        with open('users.txt', 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")

    def logout(self) -> None:
        """Logout functionality to clear the session."""
        pass  # This will be handled in the main application