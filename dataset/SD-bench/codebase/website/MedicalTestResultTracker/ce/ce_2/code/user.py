class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load(username: str):
        with open('users.txt', 'r') as file:
            for line in file:
                user, password = line.strip().split('|')
                if user == username:
                    return User(user, password)
        return None