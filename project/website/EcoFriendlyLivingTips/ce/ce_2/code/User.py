class User:
    def __init__(self, username: str, password: str, email: str):
        self._username = username
        self._password = password
        self._email = email

    def to_string(self) -> str:
        return f"{self._username}|{self._password}|{self._email}"