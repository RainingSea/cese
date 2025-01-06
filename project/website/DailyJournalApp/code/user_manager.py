class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    def exists(self) -> bool:
        with open('users.txt', 'r') as file:
            users = file.readlines()
            return any(user.split('|')[0] == self.username for user in users)

class UserManager:
    def register(self, username: str, password: str) -> bool:
        user = User(username, password)
        if not user.exists():
            user.save()
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        with open('users.txt', 'r') as file:
            users = file.readlines()
            return any(user.split('|')[0] == username and user.split('|')[1].strip() == password for user in users)

    def load_users(self) -> list:
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
        return users