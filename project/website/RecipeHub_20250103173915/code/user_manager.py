class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    def delete(self):
        pass  # Implementation for user deletion can be added later


class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file

    def load_users(self):
        users = []
        with open(self.users_file, 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users.append(User(username, password))
        return users

    def add_user(self, user: User):
        user.save()

    def delete_user(self, username: str):
        pass  # Implementation for user deletion can be added later