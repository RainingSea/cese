class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self) -> bool:
        users = load_users()
        if self.username in users:
            return False
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")
        return True

    def login(self) -> bool:
        users = load_users()
        return self.username in users and users[self.username] == self.password

def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users[username] = password
    return users