class Book:
    def __init__(self):
        self.title = ''
        self.author = ''
        self.summary = ''
        self.cover_image = ''

    @staticmethod
    def load_books():
        books = []
        with open('books.txt', 'r') as file:
            for line in file:
                title, author, summary, cover_image = line.strip().split('|')
                book = Book()
                book.title = title
                book.author = author
                book.summary = summary
                book.cover_image = cover_image
                books.append(book)
        return books

    @staticmethod
    def search_books(query: str):
        books = Book.load_books()
        return [book for book in books if query.lower() in book.title.lower()]