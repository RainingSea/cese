class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self) -> bool:
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")
        return True

    def login(self) -> bool:
        with open('users.txt', 'r') as file:
            for line in file:
                user, pwd = line.strip().split('|')
                if user == self.username and pwd == self.password:
                    return True
        return False