class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email
        }