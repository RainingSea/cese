class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class UserManager:
    def __init__(self):
        self.users = []

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')[:2]
                    self.add_user(User(username, password))
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}\n")

    def add_user(self, user: User) -> None:
        self.users.append(user)
        self.save_users()

    def authenticate(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False