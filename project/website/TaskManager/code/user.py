class User:
    def __init__(self, username: str = '', password: str = '', email: str = ''):
        self.username = username
        self.password = password
        self.email = email

    def save(self) -> None:
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")

    def load_users(self) -> list:
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    users.append(line.strip().split('|'))
        except FileNotFoundError:
            pass
        return users