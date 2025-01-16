class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self) -> None:
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load_all() -> list:
        users = []
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users.append(User(username, password))
        return users