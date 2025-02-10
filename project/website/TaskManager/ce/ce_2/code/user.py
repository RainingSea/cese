class User:
    def __init__(self, username, password, email=None):
        self.username = username
        self.password = password
        self.email = email

    def register(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}\n")
        return True

    def login(self):
        with open('users.txt', 'r') as f:
            for line in f:
                user_info = line.strip().split('|')
                if user_info[0] == self.username and user_info[1] == self.password:
                    return True
        return False