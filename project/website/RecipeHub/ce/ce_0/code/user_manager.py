class UserManager:
    def __init__(self, filename):
        self.filename = filename
        self.users = self.load_users()

    def load_users(self):
        users = []
        with open(self.filename, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append((username, password))
        return users

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users.append((username, password))
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user[0] == username and user[1] == password for user in self.users)

    def delete_account(self, username: str) -> bool:
        self.users = [user for user in self.users if user[0] != username]
        with open(self.filename, 'w') as file:
            for user in self.users:
                file.write(f"{user[0]}|{user[1]}\n")
        return True