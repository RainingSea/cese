import bcrypt

class UserManager:
    def __init__(self):
        self.users = []
        self.load_users()

    def register(self, username: str, password: str, email: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.users.append({'username': username, 'password': hashed_password.decode('utf-8'), 'email': email})
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user['username'] == username and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                return True
        return False

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    self.users.append({'username': username, 'password': password, 'email': email})
        except FileNotFoundError:
            pass

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user['username']}|{user['password']}|{user['email']}\n")