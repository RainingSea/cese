from book import Book

class BookManager:
    def __init__(self):
        self.books = Book.load_all()

    def search(self, query: str) -> list:
        """Search for books by title."""
        return [book for book in self.books if query.lower() in book.title.lower()]

    def get_book_details(self, title: str) -> Book:
        """Get details of a specific book by title."""
        for book in self.books:
            if book.title == title:
                return book
        return None