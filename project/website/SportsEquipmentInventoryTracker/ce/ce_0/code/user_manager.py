class UserManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.load_users()

    def load_users(self):
        """Load users from the text file into memory."""
        self.users = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password
        except FileNotFoundError:
            pass

    def register(self, username: str, password: str) -> bool:
        """Register a new user."""
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        """Login a user."""
        return self.users.get(username) == password