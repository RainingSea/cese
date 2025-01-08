class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

    def register_user(self, username: str, password: str):
        new_user = User(username, password)
        self.users.append(new_user)
        self.save_users()

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}\n")

    def login_user(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def delete_user(self, username: str):
        self.users = [user for user in self.users if user.username != username]
        self.save_users()