class BookManager:
    def __init__(self):
        self.books = []

    def load_books(self):
        with open('books.txt', 'r') as file:
            for line in file:
                self.books.append(line.strip())

    def search_books(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book.lower()]