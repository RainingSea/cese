class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username},{self.password},{self.email}\n")

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file

    def register(self, username: str, password: str, email: str) -> bool:
        with open(self.users_file, 'r') as file:
            users = file.readlines()
            for user in users:
                if user.split(',')[0] == username:
                    return False  # User already exists
        user = User(username, password, email)
        user.save()
        return True

    def login(self, username: str, password: str) -> bool:
        with open(self.users_file, 'r') as file:
            users = file.readlines()
            for user in users:
                user_info = user.strip().split(',')
                if user_info[0] == username and user_info[1] == password:
                    return True
        return False