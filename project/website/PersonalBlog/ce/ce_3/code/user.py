class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def to_string(self) -> str:
        return f"{self.username}|{self.password}|{self.email}"