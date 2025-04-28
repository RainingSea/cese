import os

class BookManager:
    def __init__(self, filename):
        self.filename = filename
        self.books = []

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    title, author = line.strip().split('|')
                    self.books.append((title, author))

    def add_book(self, title: str, author: str) -> bool:
        self.books.append((title, author))
        with open(self.filename, 'a') as file:
            file.write(f"{title}|{author}\n")
        return True

    def delete_book(self, title: str) -> bool:
        for book in self.books:
            if book[0] == title:
                self.books.remove(book)
                self._save_books()
                return True
        return False

    def _save_books(self):
        with open(self.filename, 'w') as file:
            for title, author in self.books:
                file.write(f"{title}|{author}\n")

    def list_books(self) -> list:
        return self.books

    def search_books(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book[0].lower()]