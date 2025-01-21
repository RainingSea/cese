class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    def validate(self):
        with open('users.txt', 'r') as f:
            for line in f:
                user, pwd = line.strip().split('|')
                if user == self.username and pwd == self.password:
                    return True
        return False