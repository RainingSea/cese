class BookManager:
    def __init__(self, books_file):
        self.books_file = books_file
        self.books = self.load_books()

    def search_books(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book['title'].lower()]

    def load_books(self) -> list:
        books = []
        try:
            with open(self.books_file, 'r') as f:
                for line in f:
                    title, author, genre = line.strip().split('|')
                    books.append({'title': title, 'author': author, 'genre': genre})
        except FileNotFoundError:
            pass
        return books