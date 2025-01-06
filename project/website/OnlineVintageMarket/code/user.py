class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self) -> bool:
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")
        return True

    def login(self) -> bool:
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    user, pwd = line.strip().split('|')
                    if user == self.username and pwd == self.password:
                        return True
        except FileNotFoundError:
            return False
        return False