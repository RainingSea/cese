import os

class Book:
    """Represents a book with title, author, summary, and cover image."""
    
    def __init__(self, title: str, author: str, summary: str, cover_image: str):
        self.title = title
        self.author = author
        self.summary = summary
        self.cover_image = cover_image

class BookManager:
    """Manages book-related functionalities such as loading and searching books."""
    
    def __init__(self):
        self.books = self.load_books()

    def load_books(self) -> list:
        """Loads books from a file into a list of Book objects."""
        if not os.path.exists('books.txt'):
            return []
        with open('books.txt', 'r') as file:
            return [self.parse_book(line.strip()) for line in file]

    def parse_book(self, line: str) -> Book:
        """Parses a line from the book file into a Book object."""
        title, author, summary, cover_image = line.split('|')
        return Book(title, author, summary, cover_image)

    def search_books(self, query: str) -> list:
        """Searches for books by title."""
        return [book for book in self.books if query.lower() in book.title.lower()]

    def get_book_details(self, title: str) -> Book:
        """Retrieves details of a specific book by title."""
        for book in self.books:
            if book.title == title:
                return book
        return None