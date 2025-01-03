class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        # Update user information in the file
        with open('users.txt', 'r') as file:
            lines = file.readlines()
        
        with open('users.txt', 'w') as file:
            for line in lines:
                if line.startswith(self.username + '|'):
                    file.write(f"{self.username}|{self.password}\n")
                else:
                    file.write(line)

    @staticmethod
    def load(username: str):
        with open('users.txt', 'r') as file:
            for line in file:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return User(user_data[0], user_data[1])
        return None