class UserManager:
    def __init__(self):
        self.users = self.load_users()
        self.profiles = self.load_profiles()

    def load_users(self):
        users = {}
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        except FileNotFoundError:
            pass
        return users

    def load_profiles(self):
        profiles = {}
        try:
            with open('profiles.txt', 'r') as file:
                for line in file:
                    username, bio = line.strip().split('|')
                    profiles[username] = bio
        except FileNotFoundError:
            pass
        return profiles

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        self.profiles[username] = ''
        with open('profiles.txt', 'a') as file:
            file.write(f"{username}| \n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def update_profile(self, username: str, bio: str) -> bool:
        if username in self.profiles:
            self.profiles[username] = bio
            with open('profiles.txt', 'w') as file:
                for user, bio in self.profiles.items():
                    file.write(f"{user}|{bio}\n")
            return True
        return False