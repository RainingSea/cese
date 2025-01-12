from user import User

class Profile:
    def __init__(self, username: str):
        self.user = self.load_user(username)

    def load_user(self, username: str):
        users = User.load_users()
        for user in users:
            if user.username == username:
                return user
        return None

    def view_profile(self):
        if self.user:
            return {
                'username': self.user.username,
                'email': self.user.email
            }
        return {}

    def edit_profile(self, username: str, email: str):
        if self.user:
            self.user.username = username
            self.user.email = email
            self.save_user()

    def save_user(self):
        users = User.load_users()
        with open('users.txt', 'w') as file:
            for user in users:
                if user.username == self.user.username:
                    file.write(f"{self.user.username}|{self.user.password}|{self.user.email}\n")
                else:
                    file.write(f"{user.username}|{user.password}|{user.email}\n")