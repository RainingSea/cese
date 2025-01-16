class User:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append((username, password))
        except FileNotFoundError:
            pass
        return users

    def save(self, username, password):
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users.append((username, password))