class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    @staticmethod
    def load_all():
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

    def update_profile(self, new_username: str, new_email: str):
        users = self.load_all()
        with open('users.txt', 'w') as f:
            for user in users:
                if user.username == self.username:
                    f.write(f"{new_username}|{self.password}\n")  # Update username
                else:
                    f.write(f"{user.username}|{user.password}\n")
        # Note: Email is not stored in the current implementation