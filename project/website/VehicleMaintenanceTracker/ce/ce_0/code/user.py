class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load_users() -> list:
        try:
            with open('users.txt', 'r') as f:
                return [User(*line.strip().split('|')) for line in f.readlines()]
        except FileNotFoundError:
            return []