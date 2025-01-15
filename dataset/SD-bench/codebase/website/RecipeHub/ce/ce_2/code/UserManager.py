from User import User

class UserManager:
    def __init__(self, users_file: str = 'users.txt'):
        self.users_file = users_file

    def load_users(self):
        users = []
        with open(self.users_file, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
        return users

    def add_user(self, user: User):
        user.save()

    def delete_user(self, username: str):
        user = User(username, '')
        user.delete()