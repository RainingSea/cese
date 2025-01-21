class ReadingList:
    def __init__(self, user):
        self.user = user
        self.books = []

    def add_book(self, book):
        """Add a book to the reading list."""
        self.books.append(book)

    def remove_book(self, book):
        """Remove a book from the reading list."""
        self.books.remove(book)

    def load(self) -> list:
        """Load the reading list."""
        return self.books