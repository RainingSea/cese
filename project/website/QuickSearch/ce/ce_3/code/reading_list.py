from user import User
from book import Book

class ReadingList:
    def __init__(self, user: User):
        self._user = user
        self._books = []

    def add_book(self, book: Book) -> None:
        self._books.append(book)

    def remove_book(self, book: Book) -> None:
        self._books.remove(book)

    def get_books(self) -> list:
        return self._books