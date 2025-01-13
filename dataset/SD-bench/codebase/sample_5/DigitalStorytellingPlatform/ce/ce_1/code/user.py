class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def register(self, username: str, password: str, email: str) -> bool:
        with open('users.txt', 'a') as file:
            file.write(f"{username},{password},{email}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return username in users and users[username][0] == password