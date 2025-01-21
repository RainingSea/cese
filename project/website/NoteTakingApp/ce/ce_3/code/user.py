class User:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append({'username': username, 'password': password})
        return users

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")