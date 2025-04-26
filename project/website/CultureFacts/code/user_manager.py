class UserManager:
    def __init__(self):
        self.users = []

    def register(self, username: str, password: str) -> bool:
        if any(user.split('|')[0] == username for user in self.users):
            return False
        self.users.append(f"{username}|{password}")
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user.split('|') == [username, password] for user in self.users)

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                self.users = file.read().strip().splitlines()
        except FileNotFoundError:
            self.users = []

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            file.write('\n'.join(self.users))