from user import User

class Profile:
    def __init__(self, username: str):
        self.user = self.load_user(username)

    def load_user(self, username: str) -> User:
        users = User.load_users()
        for user in users:
            if user.username == username:
                return user
        return None

    def view_profile(self) -> dict:
        return {
            'username': self.user.username,
            'email': self.user.email
        }

    def edit_profile(self, username: str, email: str) -> None:
        self.user.username = username
        self.user.email = email
        # Update the user file
        users = User.load_users()
        with open('users.txt', 'w') as file:
            for user in users:
                if user.username == self.user.username:
                    file.write(f"{self.user.username}|{self.user.password}|{self.user.email}\n")
                else:
                    file.write(f"{user.username}|{user.password}|{user.email}\n")