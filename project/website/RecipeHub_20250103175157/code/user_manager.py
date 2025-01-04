class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file

    def register(self, username: str, password: str) -> bool:
        if self.login(username, password):
            return False
        user = User(username, password)
        user.save()
        return True

    def login(self, username: str, password: str) -> bool:
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

    def delete_account(self, username: str):
        users = []
        with open(self.users_file, 'r') as f:
            users = f.readlines()
        with open(self.users_file, 'w') as f:
            for user in users:
                if user.split('|')[0] != username:
                    f.write(user)