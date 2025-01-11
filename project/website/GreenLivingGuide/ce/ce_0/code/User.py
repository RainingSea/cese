class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password": self.password
        }