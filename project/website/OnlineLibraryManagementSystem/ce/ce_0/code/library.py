from user import User
from book import Book

class Library:
    def __init__(self):
        self.users = []
        self.books = []

    def add_user(self, user: User):
        self.users.append(user)

    def delete_user(self, username: str):
        self.users = [user for user in self.users if user.username != username]

    def add_book(self, book: Book):
        self.books.append(book)

    def delete_book(self, title: str):
        self.books = [book for book in self.books if book.title != title]

    def view_users(self):
        return self.users

    def view_books(self):
        return self.books

    def search_books(self, query: str):
        return [book for book in self.books if query.lower() in book.title.lower() or query.lower() in book.author.lower()]

    def load_users_from_file(self, file_path: str):
        with open(file_path, 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                self.add_user(User(username, password))

    def load_books_from_file(self, file_path: str):
        with open(file_path, 'r') as file:
            for line in file:
                title, author = line.strip().split('|')
                self.add_book(Book(title, author))

    def save_users_to_file(self, file_path: str):
        with open(file_path, 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}\n")

    def save_books_to_file(self, file_path: str):
        with open(file_path, 'w') as file:
            for book in self.books:
                file.write(f"{book.title}|{book.author}\n")