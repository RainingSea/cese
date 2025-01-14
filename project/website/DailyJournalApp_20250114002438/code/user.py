class User:
    def __init__(self, username: str, password: str):
        """Initialize a User instance."""
        self.username = username
        self.password = password

    def save(self) -> bool:
        """Save the user to the users.txt file."""
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")
        return True

    def validate(self, username: str, password: str) -> bool:
        """Validate the user's credentials."""
        return self.username == username and self.password == password