from User import User

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self) -> list:
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

    def add_user(self, user: User) -> None:
        self.users.append(user)
        user.save()

    def find_user(self, username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user
        return None