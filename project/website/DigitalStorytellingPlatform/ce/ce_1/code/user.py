class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def save(self) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{self.username},{self.password},{self.email}\n")

    def validate_login(self, username: str, password: str) -> bool:
        return self.username == username and self.password == password