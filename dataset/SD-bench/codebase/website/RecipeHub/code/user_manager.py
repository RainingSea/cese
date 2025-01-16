class UserManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.users = {}
        self.load_users()

    def load_users(self):
        """Load users from the specified file."""
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password
        except FileNotFoundError:
            pass

    def register(self, username: str, password: str) -> bool:
        """Register a new user if the username is not already taken."""
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        """Check if the username and password match."""
        return self.users.get(username) == password

    def delete_account(self, username: str) -> bool:
        """Delete the user's account if it exists."""
        if username not in self.users:
            return False
        del self.users[username]
        self.save_users()
        return True

    def save_users(self):
        """Save all users to the specified file."""
        with open(self.filename, 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")

    def get_all_users(self) -> list:
        """Return a list of all registered usernames."""
        return list(self.users.keys())