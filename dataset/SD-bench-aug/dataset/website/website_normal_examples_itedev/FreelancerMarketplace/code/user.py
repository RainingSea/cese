class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        pass  # Saving is handled in main.py

    @staticmethod
    def load_all() -> list:
        return []  # Loading is handled in main.py