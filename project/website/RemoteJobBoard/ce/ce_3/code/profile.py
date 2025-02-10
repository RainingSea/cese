from user import User

class Profile:
    def __init__(self):
        self.user = None

    def view_profile(self) -> dict:
        return {
            'username': self.user.username,
            'email': self.user.email,
            'applied_jobs': self.user.applied_jobs
        }

    def edit_profile(self, username: str, email: str) -> None:
        self.user.username = username
        self.user.email = email
        # Save changes to the user data file
        users = User.load_all()
        with open('users.txt', 'w') as f:
            for user in users:
                if user.username == self.user.username:
                    f.write(f"{username}|{user.password}|{email}\n")
                else:
                    f.write(f"{user.username}|{user.password}|{user.email}\n")