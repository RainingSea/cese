from typing import List

class User:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def save(self) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{self.username},{self.password}\n")

    @staticmethod
    def load_all() -> List['User']:
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split(',')
                users.append(User(username, password))
        return users