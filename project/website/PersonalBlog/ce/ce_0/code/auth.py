from models import User

class Auth:
    """Handles user authentication."""
    @staticmethod
    def login(username: str, password: str) -> bool:
        """Log in a user."""
        users = User.load_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                return True
        return False

    @staticmethod
    def register(username: str, password: str, email: str) -> bool:
        """Register a new user."""
        existing_users = User.load_users()
        if any(user['username'] == username for user in existing_users):
            return False
        new_user = User(username, password, email)
        new_user.save()
        return True