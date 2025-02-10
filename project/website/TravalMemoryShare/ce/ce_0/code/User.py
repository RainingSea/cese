class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        pass  # Saving is handled by DataManager