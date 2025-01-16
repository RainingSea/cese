class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        pass  # Not used in this implementation

    def load(self, username: str):
        pass  # Not used in this implementation