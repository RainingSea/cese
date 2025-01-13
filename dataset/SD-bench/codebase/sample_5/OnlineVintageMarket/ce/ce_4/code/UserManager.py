class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def to_string(self) -> str:
        return f"{self.username}|{self.password}"

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.users = self.load_users()

    def register_user(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username:
                return False
        new_user = User(username, password)
        self.users.append(new_user)
        self.save_users()
        return True

    def login_user(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def load_users(self) -> list[User]:
        users = []
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

    def save_users(self) -> None:
        with open(self.users_file, 'w') as file:
            for user in self.users:
                file.write(user.to_string() + '\n')