class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    def validate(self) -> bool:
        with open('users.txt', 'r') as file:
            users = file.readlines()
            return any(user.strip().split('|')[0] == self.username and user.strip().split('|')[1] == self.password for user in users)