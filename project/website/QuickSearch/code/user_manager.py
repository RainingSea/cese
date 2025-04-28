class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file

    def register(self, username: str, password: str) -> bool:
        if self._is_username_taken(username):
            return False
        with open(self.users_file, 'a') as f:
            f.write(f"{username},{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split(',')
                if stored_username == username and stored_password == password:
                    return True
        return False

    def get_reading_list(self, username: str) -> list:
        reading_list = []
        try:
            with open('reading_list.txt', 'r') as f:
                for line in f:
                    user, book_title = line.strip().split(',')
                    if user == username:
                        reading_list.append(book_title)
        except FileNotFoundError:
            pass
        return reading_list

    def add_to_reading_list(self, username: str, book_title: str) -> None:
        with open('reading_list.txt', 'a') as f:
            f.write(f"{username},{book_title}\n")

    def _is_username_taken(self, username: str) -> bool:
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_username, _ = line.strip().split(',')
                if stored_username == username:
                    return True
        return False