import os
from user import User

class Book:
    def __init__(self, title: str, author: str, summary: str, cover_image: str):
        self.title = title
        self.author = author
        self.summary = summary
        self.cover_image = cover_image

    def get_details(self):
        return {
            "title": self.title,
            "author": self.author,
            "summary": self.summary,
            "cover_image": self.cover_image
        }

class BookManager:
    books_file = 'books.txt'

    def load_books(self):
        books = []
        if os.path.exists(self.books_file):
            with open(self.books_file, 'r') as file:
                for line in file:
                    title, author, summary, cover_image = line.strip().split('|')
                    books.append(Book(title, author, summary, cover_image))
        return books

    def search_books(self, query: str):
        return [book for book in self.load_books() if query.lower() in book.title.lower()]

    def get_book_details(self, title: str):
        for book in self.load_books():
            if book.title == title:
                return book
        return None