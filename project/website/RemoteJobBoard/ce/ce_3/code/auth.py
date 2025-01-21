class Auth:
    def login(self, username: str, password: str) -> bool:
        with open('users.txt', 'r') as file:
            for line in file:
                user_data = line.strip().split('|')
                if user_data[0] == username and user_data[1] == password:
                    return True
        return False

    def register(self, username: str, password: str, email: str) -> bool:
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        return True

    def logout(self) -> None:
        pass