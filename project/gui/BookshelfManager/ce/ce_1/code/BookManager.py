import json
from typing import List
from Book import Book

class BookManager:
    def __init__(self):
        self.books = []
        self.load_books()

    def add_book(self, title: str, author: str, genre: str, year: int, notes: str, rating: float):
        new_book = Book(title, author, genre, year, notes, rating)
        self.books.append(new_book)
        self.save_books()

    def search_books(self, query: str) -> List[Book]:
        return [book for book in self.books if query.lower() in book.title.lower() or query.lower() in book.author.lower()]

    def filter_books(self, criteria: dict) -> List[Book]:
        filtered_books = self.books
        if 'genre' in criteria:
            filtered_books = [book for book in filtered_books if book.genre == criteria['genre']]
        if 'year' in criteria:
            filtered_books = [book for book in filtered_books if book.year == criteria['year']]
        return filtered_books

    def generate_report(self) -> str:
        report = ""
        for book in self.books:
            report += f"{book.title} by {book.author}, Genre: {book.genre}, Year: {book.year}, Rating: {book.rating}\n"
        return report

    def load_books(self):
        try:
            with open('books.txt', 'r') as file:
                for line in file:
                    title, author, genre, year, notes, rating = line.strip().split('|')
                    self.books.append(Book(title, author, genre, int(year), notes, float(rating)))
        except FileNotFoundError:
            pass

    def save_books(self):
        with open('books.txt', 'w') as file:
            for book in self.books:
                file.write(f"{book.title}|{book.author}|{book.genre}|{book.year}|{book.notes}|{book.rating}\n")