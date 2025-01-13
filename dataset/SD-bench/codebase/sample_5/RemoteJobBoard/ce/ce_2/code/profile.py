from auth import Auth

class Profile:
    def __init__(self):
        self.auth = Auth()

    def view_profile(self) -> dict:
        username = self.auth.get_current_user()
        if username:
            return self.auth.users[username]
        return {}

    def edit_profile(self, username: str, email: str) -> None:
        if username in self.auth.users:
            self.auth.users[username]['email'] = email
            self.save_users()

    def save_users(self):
        with open(self.auth.users_file, 'w') as file:
            for username, data in self.auth.users.items():
                file.write(f"{username}|{data['password']}|{data['email']}\n")