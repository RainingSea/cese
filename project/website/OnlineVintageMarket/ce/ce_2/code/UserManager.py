class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


class UserManager:
    def __init__(self):
        self.users = []
        self.load_users()

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users.append(User(username, password))
        except FileNotFoundError:
            pass

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}\n")

    def register_user(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        self.users.append(new_user)
        self.save_users()
        return True

    def authenticate_user(self, username: str, password: str) -> bool:
        return any(user.username == username and user.password == password for user in self.users)