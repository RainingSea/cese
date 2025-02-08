class User:
    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password

    def register(self, username: str, password: str) -> bool:
        # Registration logic can be handled in main.py
        return True

    def login(self, username: str, password: str) -> bool:
        return self._username == username and self._password == password