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


class AuthManager:
    """Manages user authentication."""
    def register(self, username: str, password: str) -> bool:
        """Registers a new user."""
        if self.user_exists(username):
            return False
        user = User(username, password)
        user.save()
        return True

    def login(self, username: str, password: str) -> bool:
        """Logs in a user."""
        with open('users.txt', 'r') as file:
            for line in file:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

    def user_exists(self, username: str) -> bool:
        """Checks if a user exists."""
        with open('users.txt', 'r') as file:
            for line in file:
                stored_username, _ = line.strip().split('|')
                if stored_username == username:
                    return True
        return False