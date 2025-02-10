class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.users = self.load_users()

    def load_users(self) -> list:
        users = []
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append({'username': username, 'password': password})
        except FileNotFoundError:
            pass
        return users

    def register_user(self, username: str, password: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users.append({'username': username, 'password': password})
        return True

    def login_user(self, username: str, password: str) -> bool:
        return any(user['username'] == username and user['password'] == password for user in self.users)