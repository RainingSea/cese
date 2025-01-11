class UserManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.users = self.load_users()

    def register(self, username: str, password: str, email: str) -> bool:
        """Registers a new user if the username is not already taken."""
        if username in self.users:
            return False
        self.users[username] = (password, email)
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        """Logs in a user by checking username and password."""
        return username in self.users and self.users[username][0] == password

    def load_users(self) -> dict:
        """Loads users from the specified file."""
        users = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    users[username] = (password, email)
        except FileNotFoundError:
            pass
        return users

    def save_users(self) -> None:
        """Saves the current users to the specified file."""
        with open(self.filename, 'w') as file:
            for username, (password, email) in self.users.items():
                file.write(f"{username}|{password}|{email}\n")