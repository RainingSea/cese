class User:
    def __init__(self, username='', password=''):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    def load_users(self):
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

    def register(self, username, password):
        for user in self.load_users():
            if user.username == username:
                return False  # Username already exists.
        new_user = User(username, password)
        new_user.save()  # Save new user to 'users.txt'.
        return True  # Registration successful.

    def authenticate(self, username, password):
        for user in self.load_users():
            if user.username == username and user.password == password:
                return True
        return False