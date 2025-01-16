class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.users = self.load_users()

    def load_users(self) -> list:
        users = []
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

    def register(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        new_user.save()
        self.users.append(new_user)
        return True

    def login(self, username: str, password: str) -> bool:
        user = next((user for user in self.users if user.username == username), None)
        if user and user.password == password:
            return True
        return False