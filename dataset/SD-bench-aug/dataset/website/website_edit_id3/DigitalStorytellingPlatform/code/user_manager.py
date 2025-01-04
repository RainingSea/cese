class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}|{self.email}\n")

class UserManager:
    def register(self, username: str, password: str, email: str) -> bool:
        user = User(username, password, email)
        user.save()
        return True

    def login(self, username: str, password: str) -> bool:
        with open('users.txt', 'r') as file:
            for line in file:
                stored_username, stored_password, _ = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False