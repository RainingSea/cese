class BookManager:
    def __init__(self, books_file: str):
        self.books_file = books_file
        self.books = self._load_books()

    def _load_books(self) -> dict:
        books = {}
        try:
            with open(self.books_file, 'r') as f:
                for line in f:
                    title, author, summary, cover_image = line.strip().split(',')
                    books[title] = {
                        'author': author,
                        'summary': summary,
                        'cover_image': cover_image
                    }
        except FileNotFoundError:
            pass
        return books

    def search_books(self, query: str) -> list:
        results = []
        for title in self.books:
            if query.lower() in title.lower():
                results.append(title)
        return results

    def get_book_details(self, title: str) -> dict:
        return self.books.get(title, {})