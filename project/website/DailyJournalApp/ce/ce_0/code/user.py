class User:
    def __init__(self, username: str = None, password: str = None):
        self.username = username
        self.password = password

    def save(self) -> None:
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    def load_users(self) -> list:
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append({'username': username, 'password': password})
        except FileNotFoundError:
            pass  # File does not exist yet
        return users