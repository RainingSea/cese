class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        """Load users from the specified file into memory."""
        self.users = {}
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    self.users[username] = (password, email)
        except FileNotFoundError:
            pass

    def register(self, username: str, password: str, email: str) -> bool:
        """Register a new user with the given username, password, and email."""
        if username in self.users:
            return False
        self.users[username] = (password, email)
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        """Log in a user with the given username and password."""
        if username in self.users and self.users[username][0] == password:
            return True
        return False