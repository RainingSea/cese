class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append((username, password))
        except FileNotFoundError:
            pass
        return users

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users.append((username, password))
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user[0] == username and user[1] == password for user in self.users)