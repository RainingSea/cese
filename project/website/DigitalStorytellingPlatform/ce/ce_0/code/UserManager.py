class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file

    def load_users(self):
        users = []
        with open(self.users_file, 'r') as f:
            for line in f:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
        return users

    def register_user(self, username: str, password: str, email: str) -> bool:
        users = self.load_users()
        if any(user.username == username for user in users):
            return False
        new_user = User(username, password, email)
        new_user.save()
        return True

    def authenticate(self, username: str, password: str) -> bool:
        users = self.load_users()
        return any(user.username == username and user.password == password for user in users)