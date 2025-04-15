class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @staticmethod
    def load_users() -> list:
        users = []
        try:
            with open('users.txt') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

class UserController:
    def login_user(self, username: str, password: str) -> bool:
        users = User.load_users()
        for user in users:
            if user.username == username and user.password == password:
                return True
        return False

    def register_user(self, username: str, password: str) -> bool:
        users = User.load_users()
        if any(user.username == username for user in users):
            return False  # Username already exists
        new_user = User(username, password)
        new_user.save()
        return True