from book import Book

class BookManager:
    def __init__(self):
        self.books = self.load_books()

    def load_books(self) -> list:
        books = []
        with open('books.txt', 'r') as file:
            for line in file:
                title, author, summary = line.strip().split('|')
                books.append(Book(title, author, summary))
        return books

    def search_books(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book.title.lower()]

    def add_to_reading_list(self, book: Book) -> bool:
        # Placeholder for adding to reading list logic
        return True