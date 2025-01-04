class User:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def save(self) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

class UserManager:
    def __init__(self) -> None:
        self.users = []

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users.append(User(username, password))
        except FileNotFoundError:
            pass

    def add_user(self, username: str, password: str) -> None:
        user = User(username, password)
        user.save()
        self.users.append(user)

    def authenticate(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False