class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def register_user(self, username: str, password: str, email: str) -> bool:
        if username in [user.username for user in self.users]:
            return False
        new_user = User(username, password, email)
        self.users.append(new_user)
        self.save_users()
        return True

    def login_user(self, username: str, password: str) -> bool:
        return any(user.username == username and user.password == password for user in self.users)

    def load_users(self) -> list:
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass
        return users

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}|{user.email}\n")