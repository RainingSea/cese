class BookManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.books = self.load_books()

    def search_books(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book['title'].lower()]

    def get_book_details(self, title: str) -> dict:
        for book in self.books:
            if book['title'] == title:
                return book
        return {}

    def load_books(self) -> list:
        books = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    title, author, summary, cover_image = line.strip().split('|')
                    books.append({
                        'title': title,
                        'author': author,
                        'summary': summary,
                        'cover_image': cover_image
                    })
        except FileNotFoundError:
            pass
        return books