class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    def exists(self) -> bool:
        with open('users.txt', 'r') as f:
            return any(line.startswith(self.username + '|') for line in f)

class UserManager:
    def register(self, username: str, password: str) -> bool:
        user = User(username, password)
        if not user.exists():
            user.save()
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

    def load_users(self) -> list:
        users = []
        with open('users.txt', 'r') as f:
            for line in f:
                username, _ = line.strip().split('|')
                users.append(username)
        return users