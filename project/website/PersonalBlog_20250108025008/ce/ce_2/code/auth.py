class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")

    @staticmethod
    def load_all() -> list:
        users = []
        with open('users.txt', 'r') as f:
            for line in f:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
        return users


class Auth:
    def login(self, username: str, password: str) -> bool:
        users = User.load_all()
        for user in users:
            if user.username == username and user.password == password:
                return True
        return False

    def register(self, username: str, password: str, email: str) -> bool:
        users = User.load_all()
        if any(user.username == username for user in users):
            return False
        new_user = User(username, password, email)
        new_user.save()
        return True

    def logout(self):
        pass  # Placeholder for logout functionality