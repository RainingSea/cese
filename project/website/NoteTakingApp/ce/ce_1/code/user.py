class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self) -> bool:
        with open('users.txt', 'a') as file:
            file.write(f'{self.username}:{self.password}\n')
        return True

    def validate_password(self, password: str) -> bool:
        return self.password == password