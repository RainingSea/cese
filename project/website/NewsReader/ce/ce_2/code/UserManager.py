class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def validate_password(self, password: str) -> bool:
        return self.password == password

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username},{self.password}\n")


class UserManager:
    def __init__(self):
        self.users = []
        self.load_users()

    def load_users(self):
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    self.users.append(User(username, password))
        except FileNotFoundError:
            pass

    def register_user(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)
        return True

    def login_user(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.validate_password(password):
                return True
        return False