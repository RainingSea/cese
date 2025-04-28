class UserManager:
    def __init__(self):
        self.users = []

    def load_users(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users.append((username, password))

    def login(self, username: str, password: str) -> bool:
        return (username, password) in self.users

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append((username, password))
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True