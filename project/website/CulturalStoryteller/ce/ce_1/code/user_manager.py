from models import User

class UserManager:
    def register(self, username: str, password: str) -> bool:
        users = self.load_users()
        if any(user.username == username for user in users):
            return False
        new_user = User(username, password)
        new_user.save()
        return True

    def login(self, username: str, password: str) -> bool:
        users = self.load_users()
        return any(user.username == username and user.password == password for user in users)

    def load_users(self) -> list:
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users