class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password, bio = line.strip().split(',')
                users.append({'username': username, 'password': password, 'bio': bio})
        return users

    def register(self, username: str, password: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        self.users.append({'username': username, 'password': password, 'bio': ''})
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user['username']},{user['password']},{user['bio']}\n")

    def login(self, username: str, password: str) -> bool:
        return any(user['username'] == username and user['password'] == password for user in self.users)

    def update_profile(self, username: str, bio: str) -> bool:
        for user in self.users:
            if user['username'] == username:
                user['bio'] = bio
                self.save_users()
                return True
        return False