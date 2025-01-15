class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    def delete(self):
        users = []
        with open('users.txt', 'r') as f:
            users = [line.strip() for line in f if line.strip().split('|')[0] != self.username]
        with open('users.txt', 'w') as f:
            for user in users:
                f.write(user + '\n')