class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}|{self.email}\n")

    @staticmethod
    def load_users() -> list:
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    users.append(User(username, password, email))
        except FileNotFoundError:
            pass
        return users


class UserManager:
    def __init__(self):
        self.users = User.load_users()

    def register(self, username: str, password: str, email: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password, email)
        new_user.save()
        self.users.append(new_user)
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user.username == username and user.password == password for user in self.users)

    def create_new_story(self, title: str, content: str, username: str) -> None:
        if username not in [user.username for user in self.users]:
            raise ValueError("User not found.")
        story_manager.create_story(username, title, content)

    def get_all_users(self) -> list:
        return self.users

    def get_user_by_username(self, username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user
        return None