from user import User

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file

    def load_users(self) -> list:
        users = []
        with open(self.users_file, 'r') as file:
            for line in file:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
        return users

    def save_user(self, user: User) -> None:
        user.save()

    def authenticate(self, username: str, password: str) -> bool:
        users = self.load_users()
        for user in users:
            if user.username == username and user.password == password:
                return True
        return False