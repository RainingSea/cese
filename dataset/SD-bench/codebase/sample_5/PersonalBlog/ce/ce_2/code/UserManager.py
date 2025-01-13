class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{self.username},{self.password},{self.email}\n")


class UserManager:
    def register(self, username: str, password: str, email: str) -> bool:
        users = self.load_users()
        if username not in [user.username for user in users]:
            user = User(username, password, email)
            user.save()
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        users = self.load_users()
        for user in users:
            if user.username == username and user.password == password:
                return True
        return False

    def load_users(self) -> list:
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split(',')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass
        return users