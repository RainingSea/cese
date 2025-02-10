class User:
    def __init__(self, username: str, preferences: dict):
        self.username = username
        self.preferences = preferences

class UserManager:
    def __init__(self):
        self.users = []
        self.load_users()

    def create_user(self, username: str, preferences: dict) -> None:
        new_user = User(username, preferences)
        self.users.append(new_user)
        self.save_users()

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, preferences = line.strip().split('|')
                    self.users.append(User(username, eval(preferences)))
        except FileNotFoundError:
            pass

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.preferences}\n")