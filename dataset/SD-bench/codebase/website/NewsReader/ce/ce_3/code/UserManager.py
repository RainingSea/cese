class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def register(self) -> bool:
        return True  # Placeholder for registration logic

    def login(self) -> bool:
        return True  # Placeholder for login logic


class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file

    def load_users(self) -> list:
        users = []
        with open(self.users_file, 'r') as file:
            for line in file:
                username, password = line.strip().split(',')
                users.append(User(username, password))
        return users

    def save_user(self, user: User) -> None:
        with open(self.users_file, 'a') as file:
            file.write(f"{user.username},{user.password}\n")