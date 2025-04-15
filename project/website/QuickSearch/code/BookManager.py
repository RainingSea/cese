import os

class BookManager:
    """Manages book records and search functionality."""
    books_file = 'books.txt'

    def __init__(self):
        """Initialize BookManager and load books from file."""
        self.books = self.load_books()

    def load_books(self) -> dict:
        """Load books from a file."""
        books_dict = {}
        if os.path.exists(self.books_file):
            with open(self.books_file, 'r') as file:
                for line in file:
                    title, author, genre = line.strip().split('|')
                    books_dict[title] = {'author': author, 'genre': genre}
        return books_dict

    def search_books(self, query: str) -> list:
        """Search for books by title or author."""
        results = []
        for title, details in self.books.items():
            if query.lower() in title.lower() or query.lower() in details['author'].lower():
                results.append(title)
        return results

    def get_book_details(self, title: str) -> dict:
        """Get details of a specific book."""
        return self.books.get(title, {})