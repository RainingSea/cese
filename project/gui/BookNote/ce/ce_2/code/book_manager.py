import os
from models import Book

class BookManager:
    def __init__(self):
        self.books = []
        self.load_books()

    def add_book(self, title: str, author: str, genre: str, publication_date: str):
        new_book = Book(title, author, genre, publication_date)
        self.books.append(new_book)
        self.save_books()

    def load_books(self):
        if os.path.exists('books.txt'):
            with open('books.txt', 'r') as file:
                for line in file:
                    title, author, genre, publication_date = line.strip().split('|')
                    self.books.append(Book(title, author, genre, publication_date))

    def save_books(self):
        with open('books.txt', 'w') as file:
            for book in self.books:
                file.write(f"{book.title}|{book.author}|{book.genre}|{book.publication_date}\n")