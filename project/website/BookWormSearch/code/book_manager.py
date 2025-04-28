import os

class BookManager:
    def __init__(self, books_file: str):
        self.books_file = books_file
        self.load_books()

    def load_books(self):
        self.books = {}
        if os.path.exists(self.books_file):
            with open(self.books_file, 'r') as file:
                for line in file:
                    title, author, description = line.strip().split('|')
                    self.books[title] = {'author': author, 'description': description}

    def search_books(self, query: str) -> list:
        return [title for title in self.books if query.lower() in title.lower()]

    def get_book_details(self, title: str) -> dict:
        return self.books.get(title, {})