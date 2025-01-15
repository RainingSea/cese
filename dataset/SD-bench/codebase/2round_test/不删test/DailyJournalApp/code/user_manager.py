import bcrypt

class User:
    def __init__(self, username: str, password: bytes):
        self.username = username
        self.password = password

    def save(self) -> None:
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password.decode('utf-8')}\n")

    def validate(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password)


class UserManager:
    def __init__(self):
        self.users = []

    def register(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(username, hashed_password)
        new_user.save()
        self.users.append(new_user)
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.validate(password):
                return True
        return False

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    self.users.append(User(username, password.encode('utf-8')))
        except FileNotFoundError:
            pass

    def cleanup_users(self) -> None:
        open('users.txt', 'w').close()  # Clear the user file