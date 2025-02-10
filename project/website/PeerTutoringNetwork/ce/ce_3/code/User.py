class User:
    def __init__(self, username: str, password: str, email: str) -> None:
        self.username = username
        self.password = password
        self.email = email

    def save(self) -> None:
        pass  # Saving is handled by FileManager