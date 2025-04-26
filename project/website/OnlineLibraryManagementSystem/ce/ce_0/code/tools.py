class UserManager:
    def __init__(self):
        self.users = []
        self.load_users()

    def register(self, username: str, password: str) -> None:
        self.users.append(f"{username}|{password}")
        self.save_users()

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            stored_username, stored_password = user.split('|')
            if stored_username == username and stored_password == password:
                return True
        return False

    def logout(self) -> None:
        session.pop('username', None)

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                self.users = file.read().strip().split('\n')
        except FileNotFoundError:
            self.users = []

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            file.write('\n'.join(self.users))


class BookManager:
    def __init__(self):
        self.books = []
        self.load_books()

    def add_book(self, title: str, author: str) -> None:
        self.books.append(f"{title}|{author}")
        self.save_books()

    def delete_book(self, title: str) -> None:
        self.books = [book for book in self.books if not book.startswith(title)]
        self.save_books()

    def view_books(self) -> list:
        return self.books

    def load_books(self) -> None:
        try:
            with open('books.txt', 'r') as file:
                self.books = file.read().strip().split('\n')
        except FileNotFoundError:
            self.books = []

    def save_books(self) -> None:
        with open('books.txt', 'w') as file:
            file.write('\n'.join(self.books))