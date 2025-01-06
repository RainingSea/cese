class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}|{self.email}\n")


class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file

    def register(self, username: str, password: str, email: str) -> bool:
        user = User(username, password, email)
        user.save()
        return True

    def login(self, username: str, password: str) -> bool:
        with open(self.users_file, 'r') as file:
            for line in file:
                user_data = line.strip().split('|')
                if user_data[0] == username and user_data[1] == password:
                    return True
        return False