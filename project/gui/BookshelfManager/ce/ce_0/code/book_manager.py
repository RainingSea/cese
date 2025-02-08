import json
from typing import List, Dict
from book import Book

class BookManager:
    def __init__(self):
        self.books: List[Book] = []
        self.load_books_from_file()

    def add_book(self, title: str, author: str, genre: str, year: int, shelf: str, notes: str, rating: float):
        new_book = Book(title, author, genre, year, shelf, notes, rating)
        self.books.append(new_book)
        self.save_books_to_file()

    def generate_report(self) -> Dict:
        report = {
            "total_books": len(self.books),
            "average_rating": self.get_average_rating(),
            "shelves": self.get_shelves()
        }
        return report

    def search_books(self, query: str) -> List[Book]:
        return [book for book in self.books if query.lower() in book.title.lower() or query.lower() in book.author.lower()]

    def filter_books(self, criteria: Dict) -> List[Book]:
        filtered_books = self.books
        if "genre" in criteria:
            filtered_books = [book for book in filtered_books if book.genre == criteria["genre"]]
        if "shelf" in criteria:
            filtered_books = [book for book in filtered_books if book.shelf == criteria["shelf"]]
        return filtered_books

    def load_books_from_file(self):
        try:
            with open('books.txt', 'r') as file:
                books_data = json.load(file)
                self.books = [Book(**book) for book in books_data]
        except FileNotFoundError:
            self.books = []

    def save_books_to_file(self):
        with open('books.txt', 'w') as file:
            json.dump([book.__dict__ for book in self.books], file)

    def get_average_rating(self) -> float:
        if not self.books:
            return 0.0
        return sum(book.rating for book in self.books) / len(self.books)

    def get_shelves(self) -> List[str]:
        return list(set(book.shelf for book in self.books))