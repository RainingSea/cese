from models import Book

class BookManager:
    def __init__(self, books_file: str):
        self.books_file = books_file
        self.books = self.load_books()

    def load_books(self):
        books = []
        try:
            with open(self.books_file, 'r') as file:
                for line in file:
                    title, author, content = line.strip().split('|')
                    books.append(Book(title, author, content))
        except FileNotFoundError:
            pass
        return books

    def create_book(self, title: str, author: str, content: str) -> None:
        new_book = Book(title, author, content)
        new_book.save()
        self.books.append(new_book)

    def get_books(self) -> list:
        return self.books

    def get_book_details(self, title: str) -> Book:
        for book in self.books:
            if book.title == title:
                return book
        return None