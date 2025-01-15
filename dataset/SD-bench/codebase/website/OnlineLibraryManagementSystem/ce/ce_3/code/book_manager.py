import json

class BookManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.books = self.load_books()

    def load_books(self) -> list:
        try:
            with open(self.file_path, 'r') as file:
                return [line.strip().split('|') for line in file.readlines()]
        except FileNotFoundError:
            return []

    def add_book(self, title: str, author: str) -> bool:
        if any(book[0] == title for book in self.books):
            return False
        self.books.append([title, author])
        self.save_books()
        return True

    def delete_book(self, title: str) -> bool:
        for book in self.books:
            if book[0] == title:
                self.books.remove(book)
                self.save_books()
                return True
        return False

    def get_books(self) -> list:
        return self.books

    def search_books(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book[0].lower() or query.lower() in book[1].lower()]

    def save_books(self):
        with open(self.file_path, 'w') as file:
            for book in self.books:
                file.write('|'.join(book) + '\n')