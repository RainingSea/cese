from User import User

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file

    def register(self, username: str, password: str) -> bool:
        user = User(username, password)
        user.save()
        return True

    def login(self, username: str, password: str) -> bool:
        with open(self.users_file, 'r') as user_file:
            for line in user_file:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

    def get_all_users(self) -> list:
        users = []
        with open(self.users_file, 'r') as user_file:
            for line in user_file:
                username, _ = line.strip().split('|')
                users.append(username)
        return users