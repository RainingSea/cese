class UserManager:
    def __init__(self, users_file):
        self.users_file = users_file

    def validate_user(self, username, password):
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    user_data = line.strip().split(',')
                    if user_data[0] == username and user_data[1] == password:
                        return True
        except FileNotFoundError:
            return False
        return False

    def add_user(self, username, password, email):
        if self.validate_user(username, password):
            return False
        with open(self.users_file, 'a') as file:
            file.write(f"{username},{password},{email}\n")
        return True