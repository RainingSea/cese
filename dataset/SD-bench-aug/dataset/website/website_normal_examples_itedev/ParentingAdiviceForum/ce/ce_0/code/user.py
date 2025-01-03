class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    def delete(self):
        users = []
        with open('users.txt', 'r') as file:
            users = file.readlines()
        
        with open('users.txt', 'w') as file:
            for user in users:
                if user.strip().split('|')[0] != self.username:
                    file.write(user)