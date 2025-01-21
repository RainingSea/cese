class UserProfileManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self) -> dict:
        users = {}
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = {'password': password, 'preferences': {}}
        except FileNotFoundError:
            pass
        return users

    def save_user(self, user: dict):
        self.users[user['username']] = {'password': user['password'], 'preferences': user['preferences']}
        with open('users.txt', 'a') as file:
            file.write(f"{user['username']}|{user['password']}\n")

    def get_user_preferences(self, user_id: str) -> dict:
        return self.users.get(user_id, {}).get('preferences', {})