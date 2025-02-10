import json

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self) -> bool:
        user_data = {'username': self.username, 'password': self.password}
        with open('users.txt', 'a') as file:
            file.write(json.dumps(user_data) + '\n')
        return True

    def load_all(self) -> list:
        users = []
        try:
            with open('users.txt', 'r') as file:
                users = [json.loads(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            pass
        return users