from book import Book

class BookManager:
    def __init__(self, books_file: str):
        self.books_file = books_file
        self.load_books()

    def load_books(self):
        self.books = {}
        try:
            with open(self.books_file, 'r') as file:
                for line in file:
                    username, title, author, content = line.strip().split(':')
                    book = Book(username, title, author, content)
                    if username not in self.books:
                        self.books[username] = []
                    self.books[username].append(book)
        except FileNotFoundError:
            open(self.books_file, 'w').close()  # Create file if it doesn't exist

    def add_book(self, book: Book):
        book.save()
        if book.username not in self.books:
            self.books[book.username] = []
        self.books[book.username].append(book)

    def get_books_by_user(self, username: str) -> list:
        return self.books.get(username, [])

    def get_book_details(self, title: str, username: str) -> Book:
        for book in self.books.get(username, []):
            if book.title == title:
                return book
        return None