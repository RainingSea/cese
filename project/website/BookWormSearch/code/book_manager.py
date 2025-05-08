class BookManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.books = self.load_books()

    def load_books(self):
        books = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    title, author, genre = line.strip().split('|')
                    books.append({'title': title, 'author': author, 'genre': genre})
        except FileNotFoundError:
            pass
        return books

    def search_books(self, query: str) -> list:
        query_lower = query.lower()
        results = []
        for book in self.books:
            if (query_lower in book['title'].lower() or
                query_lower in book['author'].lower()):
                results.append(book)
        return results

    def get_book_details(self, title: str) -> dict:
        for book in self.books:
            if book['title'].lower() == title.lower():
                return book
        return {}

    def get_all_books(self) -> list:
        return self.books