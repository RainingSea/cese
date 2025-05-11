class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        """Load users from the specified file."""
        self.users = {}
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password
        except FileNotFoundError:
            pass

    def register(self, username: str, password: str) -> bool:
        """Register a new user with the given username and password."""
        if username in self.users or not username or not password:
            raise ValueError("Invalid username or password.")
        self.users[username] = password
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        """Log in the user with the given username and password."""
        return self.users.get(username) == password

    def logout(self) -> None:
        """Logout logic handled in the main application."""
        pass

    def is_manager(self, username: str) -> bool:
        """Check if the user is a manager."""
        return username == "admin"