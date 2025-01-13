class User:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def save(self) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{self.username},{self.password}\n")

    def exists(self) -> bool:
        with open('users.txt', 'r') as file:
            users = file.readlines()
            return any(user.split(',')[0] == self.username for user in users)


class UserManager:
    def __init__(self):
        self.users = []
        self.load_users()

    def register(self, username: str, password: str) -> bool:
        user = User(username, password)
        if not user.exists():
            user.save()
            self.users.append(user)
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        return any(user.username == username and user.password == password for user in self.users)

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    self.users.append(User(username, password))
        except FileNotFoundError:
            pass