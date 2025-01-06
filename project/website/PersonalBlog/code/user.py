class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        pass  # Not needed for file-based storage

    @classmethod
    def load(cls, username: str):
        pass  # Not needed for file-based storage