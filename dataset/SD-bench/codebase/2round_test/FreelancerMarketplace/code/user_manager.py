class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    def validate_password(self, password: str) -> bool:
        return self.password == password


class UserManager:
    def register(self, username: str, password: str) -> bool:
        users = self.load_users()
        if any(user.username == username for user in users):
            return False
        user = User(username, password)
        user.save()
        return True

    def login(self, username: str, password: str) -> bool:
        users = self.load_users()
        user = next((user for user in users if user.username == username), None)
        return user is not None and user.validate_password(password)

    def load_users(self) -> list:
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

    def update_user(self, username: str, new_password: str) -> bool:
        users = self.load_users()
        for user in users:
            if user.username == username:
                user.password = new_password
                self.save_users(users)
                return True
        return False

    def save_users(self, users: list) -> None:
        with open('users.txt', 'w') as f:
            for user in users:
                f.write(f"{user.username}|{user.password}\n")