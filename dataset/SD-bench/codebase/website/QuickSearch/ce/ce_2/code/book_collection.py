class Book:
    def __init__(self, title: str, author: str, summary: str, cover_image: str):
        self.title = title
        self.author = author
        self.summary = summary
        self.cover_image = cover_image

    def get_details(self) -> dict:
        return {
            'title': self.title,
            'author': self.author,
            'summary': self.summary,
            'cover_image': self.cover_image
        }

class BookCollection:
    def __init__(self):
        self.books = []

    def load_books(self, file_path: str) -> list:
        with open(file_path, 'r') as file:
            for line in file:
                title, author, summary, cover_image = line.strip().split('|')
                book = Book(title, author, summary, cover_image)
                self.books.append(book)
        return self.books

    def search_books(self, query: str) -> list:
        return [book.get_details() for book in self.books if query.lower() in book.title.lower()]