class User:
    def __init__(self, username: str = '', password: str = ''):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    def load(self, username: str):
        with open('users.txt', 'r') as file:
            for line in file:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    self.username = user_data[0]
                    self.password = user_data[1]
                    return True
        return False