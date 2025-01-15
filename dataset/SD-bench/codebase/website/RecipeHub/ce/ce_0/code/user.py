class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self, username: str, password: str) -> bool:
        # Registration logic handled in main.py
        return True

    def login(self, username: str, password: str) -> bool:
        # Login logic handled in main.py
        return True