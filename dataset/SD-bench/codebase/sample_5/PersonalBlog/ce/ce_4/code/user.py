class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def register(self, username: str, password: str, email: str) -> bool:
        # Assuming registration is always successful for simplicity
        return True

    def login(self, username: str, password: str) -> bool:
        return self.username == username and self.password == password