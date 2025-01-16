class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load() -> dict:
        users = {}
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
        return users