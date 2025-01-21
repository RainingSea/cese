class Book:
    def __init__(self, title: str, author: str, summary: str):
        self.title = title
        self.author = author
        self.summary = summary

    def get_details(self):
        return {
            'title': self.title,
            'author': self.author,
            'summary': self.summary
        }

class BookManager:
    def __init__(self):
        self.books = []

    def load_books(self, file_path: str):
        with open(file_path, 'r') as file:
            for line in file:
                title, author, summary = line.strip().split('|')
                self.books.append(Book(title, author, summary))

    def search_books(self, query: str):
        return [book.get_details() for book in self.books if query.lower() in book.title.lower()]

    def get_book(self, title: str):
        for book in self.books:
            if book.title == title:
                return book.get_details()
        return None