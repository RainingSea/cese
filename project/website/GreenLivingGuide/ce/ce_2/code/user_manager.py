class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append((username, password))
        return users

    def login(self, username: str, password: str) -> bool:
        for user, pwd in self.users:
            if user == username and pwd == password:
                return True
        return False

    def create_account(self, username: str, password: str) -> bool:
        if any(user == username for user, _ in self.users):
            return False
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users.append((username, password))
        return True