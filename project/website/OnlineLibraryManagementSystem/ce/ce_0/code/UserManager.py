class UserManager:
    def __init__(self):
        self.users = []
        self.load_users()

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append((username, password))
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user[0] == username and user[1] == password for user in self.users)

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                self.users = [line.strip().split('|') for line in file.readlines()]
        except FileNotFoundError:
            self.users = []

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')