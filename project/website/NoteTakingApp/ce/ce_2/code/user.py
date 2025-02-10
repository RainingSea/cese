class User:
    def __init__(self, user_file='users.txt'):
        self.user_file = user_file

    def register(self, username: str, password: str) -> bool:
        with open(self.user_file, 'a') as f:
            f.write(f"{username},{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        with open(self.user_file, 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split(',')
                if stored_username == username and stored_password == password:
                    return True
        return False