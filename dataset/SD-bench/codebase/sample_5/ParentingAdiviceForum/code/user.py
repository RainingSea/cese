class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self) -> None:
        """Save the user to the users.txt file."""
        with open('users.txt', 'a') as file:
            file.write(f"{self.username}|{self.password}\n")

    def update_profile(self, new_username: str, new_password: str) -> None:
        """Update the user's profile."""
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                u, p = line.strip().split('|')
                if u == self.username:
                    users.append(f"{new_username}|{new_password}\n")
                else:
                    users.append(line)
        with open('users.txt', 'w') as file:
            file.writelines(users)

    def delete_account(self) -> None:
        """Delete the user's account."""
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                u, p = line.strip().split('|')
                if u != self.username:
                    users.append(line)
        with open('users.txt', 'w') as file:
            file.writelines(users)