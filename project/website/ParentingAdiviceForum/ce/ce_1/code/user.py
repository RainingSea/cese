class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    def delete(self):
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                if line.strip().split('|')[0] != self.username:
                    users.append(line.strip())
        with open('users.txt', 'w') as file:
            for user in users:
                file.write(f"{user}\n")