class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        """Save the user to the users.txt file."""
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    def validate_password(self, password: str) -> bool:
        """Validate the user's password."""
        return self.password == password