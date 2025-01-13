class User:
    def __init__(self, username: str, password: str, email: str = None):
        self.username = username
        self.password = password
        self.email = email

    def save(self) -> None:
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")

    def load_users(self) -> list:
        users = []
        with open('users.txt', 'r') as f:
            for line in f:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
        return users

    def authenticate(self) -> bool:
        users = self.load_users()
        for user in users:
            if user.username == self.username and user.password == self.password:
                return True
        return False