from models import User

class UserManager:
    def __init__(self, users_file: str = 'users.txt'):
        self.users_file = users_file

    def load_users(self):
        users = []
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return users

    def save_user(self, user: User):
        if self.find_user(user.username) is None:
            user.save()
            return True
        return False

    def find_user(self, username: str) -> User:
        users = self.load_users()
        for user in users:
            if user.username == username:
                return user
        return None