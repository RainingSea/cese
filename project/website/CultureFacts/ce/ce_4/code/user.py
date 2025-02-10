class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save_user(self) -> bool:
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")
        return True

    def validate_user(self) -> bool:
        return True if self.username and self.password else False