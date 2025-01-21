class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        """Saves the user data to the users file."""
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    def validate_password(self, password: str) -> bool:
        """Validates the user's password."""
        return self.password == password