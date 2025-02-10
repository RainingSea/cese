class User:
    def __init__(self):
        self.users_file = 'users.txt'

    def register(self, username: str, password: str) -> bool:
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        with open(self.users_file, 'r') as file:
            for line in file:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False