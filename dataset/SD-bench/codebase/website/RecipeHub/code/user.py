class User:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
        return users

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users[username] = password
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def delete_account(self, username: str) -> bool:
        if username in self.users:
            del self.users[username]
            with open('users.txt', 'w') as file:
                for user, pwd in self.users.items():
                    file.write(f"{user}|{pwd}\n")
            return True
        return False