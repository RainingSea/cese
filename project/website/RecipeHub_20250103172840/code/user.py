class User:
    def __init__(self):
        self.username = ""
        self.password = ""

    def register(self, username: str, password: str) -> bool:
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}|\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return username in users and users[username]['password'] == password

    def delete_account(self, username: str) -> bool:
        if username in users:
            del users[username]
            self.save_users()
            return True
        return False

    def save_users(self):
        with open('users.txt', 'w') as file:
            for username, data in users.items():
                file.write(f"{username}|{data['password']}|{','.join(data['entries'])}\n")