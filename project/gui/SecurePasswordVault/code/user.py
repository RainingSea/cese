class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        try:
            with open("users.txt", 'r') as user_file:
                for line in user_file:
                    username, password = line.strip().split('|')
                    users[username] = password
        except FileNotFoundError:
            pass
        return users

    def register_user(self, username: str, password: str):
        if username not in self.users:
            self.users[username] = password
            with open("users.txt", 'a') as user_file:
                user_file.write(f"{username}|{password}\n")
        else:
            raise ValueError("User already exists.")

    def login_user(self, username: str, password: str) -> bool:
        return self.users.get(username) == password