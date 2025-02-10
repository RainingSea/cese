from models import User

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.users = self.load_users()

    def load_users(self) -> dict:
        users = {}
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password, email, applied_jobs = line.strip().split('|')
                    user = User(username, password, email)
                    user.applied_jobs = applied_jobs.split(',') if applied_jobs else []
                    users[username] = user
        except FileNotFoundError:
            pass
        return users

    def register_user(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        new_user = User(username, password, email)
        self.users[username] = new_user
        with open(self.users_file, 'a') as file:
            file.write(new_user.to_string() + '\n')
        return True

    def login_user(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        return user is not None and user.password == password

    def get_user(self, username: str) -> User:
        return self.users.get(username)