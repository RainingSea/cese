import json
import os

class BookManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.books = self.load_books()

    def load_books(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r') as file:
            return json.load(file)

    def add_book(self, title: str, author: str) -> bool:
        for book in self.books:
            if book['title'] == title:
                return False
        self.books.append({'title': title, 'author': author})
        self.save_books()
        return True

    def delete_book(self, title: str) -> bool:
        for book in self.books:
            if book['title'] == title:
                self.books.remove(book)
                self.save_books()
                return True
        return False

    def get_books(self) -> list:
        return self.books

    def search_books(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book['title'].lower()]

    def save_books(self):
        with open(self.filename, 'w') as file:
            json.dump(self.books, file)