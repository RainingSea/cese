class UserManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.users = self.load_users()

    def register(self, username: str, password: str) -> bool:
        """Registers a new user if the username is not taken."""
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        """Logs in a user by checking credentials."""
        return self.users.get(username) == password

    def load_users(self) -> dict:
        """Loads users from the specified file."""
        users = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        except FileNotFoundError:
            pass
        return users

    def logout(self, session: dict) -> None:
        """Logs out a user by removing their username from the session."""
        session.pop('username', None)

    def is_username_taken(self, username: str) -> bool:
        """Checks if a username is already taken."""
        return username in self.users