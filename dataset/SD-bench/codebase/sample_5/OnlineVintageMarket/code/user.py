class User:
    """User class to represent a user."""
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def validate_password(self, password: str) -> bool:
        """Validate the user's password."""
        return self.password == password