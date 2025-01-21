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
                user, pwd = line.strip().split('|')
                if user == username and pwd == password:
                    return True
        return False