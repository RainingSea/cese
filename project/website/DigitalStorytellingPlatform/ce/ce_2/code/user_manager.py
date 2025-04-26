class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        """Load users from the users file into memory."""
        self.users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    self.users[username] = (password, email)

    def register(self, username: str, password: str, email: str) -> bool:
        """Register a new user."""
        if username in self.users:
            return False
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        self.users[username] = (password, email)
        return True

    def login(self, username: str, password: str) -> bool:
        """Log in a user."""
        return username in self.users and self.users[username][0] == password