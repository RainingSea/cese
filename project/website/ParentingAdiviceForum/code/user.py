class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def to_string(self) -> str:
        return f"{self.username}|{self.password}"

class UserManager:
    def __init__(self):
        self.users = []

    def add_user(self, user: User):
        self.users.append(user)

    def get_user(self, username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user
        return None

    def list_users(self) -> list:
        return self.users