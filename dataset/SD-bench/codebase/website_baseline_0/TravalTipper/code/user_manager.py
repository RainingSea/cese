class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.favorites = []

    def save_favorite(self, tip):
        self.favorites.append(tip)

    def get_favorites(self):
        return self.favorites


class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def register(self, username: str, password: str):
        new_user = User(username, password)
        self.users.append(new_user)
        self.save_users()

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def is_username_taken(self, username: str) -> bool:
        return any(user.username == username for user in self.users)

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

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}\n")

    def save_favorite(self, username: str, tip: str):
        for user in self.users:
            if user.username == username:
                user.save_favorite(tip)
                self.save_users()
                break

    def get_favorites(self, username: str):
        for user in self.users:
            if user.username == username:
                return user.get_favorites()
        return []