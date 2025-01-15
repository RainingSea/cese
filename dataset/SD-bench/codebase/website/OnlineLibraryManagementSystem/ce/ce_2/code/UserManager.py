class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def to_string(self) -> str:
        return f"{self.username}|{self.password}"

class UserManager:
    def __init__(self):
        self.users = []

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.add_user(User(username, password))
        except FileNotFoundError:
            pass

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(user.to_string() + '\n')

    def add_user(self, user: User) -> None:
        self.users.append(user)

    def get_users(self) -> list[User]:
        return self.users