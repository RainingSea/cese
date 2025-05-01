import os
import csv

class Book:
    def __init__(self, title, author, genre, year):
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.notes = []
        self.rating = None

class Shelf:
    def __init__(self, name):
        self.name = name
        self.books = []

class BookManager:
    def __init__(self):
        self.books = []
        self.shelves = []
        self.load_books()
        self.load_shelves()

    def add_book(self, title, author, genre, year):
        new_book = Book(title, author, genre, year)
        self.books.append(new_book)
        self.save_books()

    def add_shelf(self, name):
        new_shelf = Shelf(name)
        self.shelves.append(new_shelf)
        self.save_shelves()

    def add_note_to_book(self, book_id, note):
        if 0 <= book_id < len(self.books):
            self.books[book_id].notes.append(note)
            self.save_books()

    def rate_book(self, book_id, rating):
        if 0 <= book_id < len(self.books):
            self.books[book_id].rating = rating
            self.save_books()

    def generate_report(self):
        report_lines = ["Report of Books:"]
        for i, book in enumerate(self.books, start=1):
            report_lines.append(f"{i}. {book.title} by {book.author}")
        return "\n".join(report_lines)

    def search_books(self, query):
        return [book for book in self.books if query.lower() in book.title.lower() or query.lower() in book.author.lower()]

    def filter_books(self, criteria):
        return [book for book in self.books if book.genre == criteria]

    def load_books(self):
        if os.path.exists('books.txt'):
            with open('books.txt', 'r') as file:
                for line in file:
                    title, author, genre, year = line.strip().split('|')
                    self.books.append(Book(title, author, genre, int(year)))

    def save_books(self):
        with open('books.txt', 'w') as file:
            for book in self.books:
                file.write(f"{book.title}|{book.author}|{book.genre}|{book.year}\n")

    def load_shelves(self):
        if os.path.exists('shelves.txt'):
            with open('shelves.txt', 'r') as file:
                for line in file:
                    self.shelves.append(Shelf(line.strip()))

    def save_shelves(self):
        with open('shelves.txt', 'w') as file:
            for shelf in self.shelves:
                file.write(f"{shelf.name}\n")