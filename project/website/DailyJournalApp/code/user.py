class User:
    """Represents a user in the system."""
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self) -> None:
        """Saves the user to a file."""
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    def validate_password(self, password: str) -> bool:
        """Validates the user's password."""
        return self.password == password

class UserManager:
    """Manages user registrations and logins."""
    def __init__(self):
        self.users = []

    def register(self, username: str, password: str) -> bool:
        """Registers a new user."""
        if any(user.username == username for user in self.users):
            return False  # User already exists
        new_user = User(username, password)
        self.users.append(new_user)
        new_user.save()
        return True

    def login(self, username: str, password: str) -> bool:
        """Logs in a user."""
        for user in self.users:
            if user.username == username and user.validate_password(password):
                return True
        return False

    def load_users(self) -> None:
        """Loads users from a file."""
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users.append(User(username, password))
        except FileNotFoundError:
            pass