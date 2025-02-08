import os
from typing import List, Dict
from book import Book

class BookManager:
    def __init__(self):
        self.books = []
        self.load_books()

    def add_book(self, title: str, author: str, genre: str, year: int, notes: str, rating: float) -> None:
        new_book = Book(title, author, genre, year, notes, rating)
        self.books.append(new_book)
        self.save_books()

    def search_books(self, query: str) -> List[Book]:
        return [book for book in self.books if query.lower() in book.title.lower() or query.lower() in book.author.lower()]

    def filter_books(self, criteria: Dict[str, str]) -> List[Book]:
        filtered_books = self.books
        for key, value in criteria.items():
            filtered_books = [book for book in filtered_books if getattr(book, key, '').lower() == value.lower()]
        return filtered_books

    def generate_report(self) -> Dict[str, int]:
        report = {}
        for book in self.books:
            report[book.genre] = report.get(book.genre, 0) + 1
        return report

    def load_books(self) -> None:
        if os.path.exists('books.txt'):
            with open('books.txt', 'r') as file:
                for line in file:
                    title, author, genre, year, notes, rating = line.strip().split('|')
                    book = Book(title, author, genre, int(year), notes, float(rating))
                    self.books.append(book)

    def save_books(self) -> None:
        with open('books.txt', 'w') as file:
            for book in self.books:
                file.write(f"{book.title}|{book.author}|{book.genre}|{book.year}|{book.notes}|{book.rating}\n")