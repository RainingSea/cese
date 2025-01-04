class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

class UserManager:
    def register(self, username: str, password: str) -> bool:
        if not self.user_exists(username):
            user = User(username, password)
            user.save()
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

    def user_exists(self, username: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                stored_username, _ = line.strip().split('|')
                if stored_username == username:
                    return True
        return False

    def delete_account(self, username: str) -> None:
        users = []
        with open('users.txt', 'r') as f:
            users = f.readlines()
        with open('users.txt', 'w') as f:
            for user in users:
                if user.split('|')[0] != username:
                    f.write(user)