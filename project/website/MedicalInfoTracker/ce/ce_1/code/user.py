class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self) -> bool:
        users = self.load_all()
        if any(user.username == self.username for user in users):
            return False
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")
        return True

    def authenticate(self) -> bool:
        users = self.load_all()
        return any(user.username == self.username and user.password == self.password for user in users)

    @staticmethod
    def load_all() -> list:
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users