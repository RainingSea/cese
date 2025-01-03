class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        """Load users from the users file into memory."""
        self.users = {}
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    self.users[username] = {'password': password, 'email': email}
        except FileNotFoundError:
            pass

    def register(self, username: str, password: str, email: str) -> bool:
        """Register a new user if the username does not already exist."""
        if username in self.users:
            return False
        self.users[username] = {'password': password, 'email': email}
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        """Check if the username and password are correct for login."""
        user = self.users.get(username)
        return user is not None and user['password'] == password