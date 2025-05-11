import bcrypt

class UserManager:
    def __init__(self):
        self.users = []

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.users.append((username, hashed_password))
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and bcrypt.checkpw(password.encode('utf-8'), user[1]):
                return True
        return False

    def logout(self) -> None:
        pass

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users.append((username, password.encode('utf-8')))
        except FileNotFoundError:
            pass

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for username, password in self.users:
                file.write(f"{username}|{password.decode('utf-8')}\n")