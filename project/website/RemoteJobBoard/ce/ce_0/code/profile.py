class Profile:
    def __init__(self, user: User = None):
        self.user = user

    def view_profile(self):
        return {
            'username': self.user.username,
            'email': self.user.email
        }

    def edit_profile(self, new_data: dict):
        self.user.username = new_data.get('username', self.user.username)
        self.user.email = new_data.get('email', self.user.email)
        # Save changes to users.txt
        users = self.load_users()
        with open('users.txt', 'w') as f:
            for user in users:
                if user.username == self.user.username:
                    f.write(f"{self.user.username}|{self.user.password}|{self.user.email}\n")
                else:
                    f.write(f"{user.username}|{user.password}|{user.email}\n")

    def load_users(self):
        users = []
        with open('users.txt', 'r') as f:
            for line in f:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
        return users