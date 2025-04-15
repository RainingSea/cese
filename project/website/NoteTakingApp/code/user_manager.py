class UserManager:
    def __init__(self, user_file: str):
        self.user_file = user_file
        self.users = {}
        self.load_users()

    def load_users(self):
        """Load users from the user file into memory."""
        try:
            with open(self.user_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password
        except FileNotFoundError:
            pass

    def register(self, username: str, password: str) -> bool:
        """Register a new user if the username does not already exist."""
        if self.user_exists(username):
            return False
        self.users[username] = password
        with open(self.user_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        """Check if the username and password match."""
        return self.users.get(username) == password

    def user_exists(self, username: str) -> bool:
        """Check if a user exists in the system."""
        return username in self.users

    def logout(self):
        """Logout the current user."""
        self.users.clear()