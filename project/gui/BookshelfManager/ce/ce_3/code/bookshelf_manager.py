import os
from book import Book

class BookshelfManager:
    def __init__(self):
        self.books = []

    def add_book(self, book: Book):
        self.books.append(book)

    def load_books(self, file_path: str):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                for line in file:
                    title, author, genre, publication_year, notes, rating = line.strip().split(',')
                    book = Book(title, author, genre, int(publication_year))
                    book.add_notes(notes)
                    book.add_rating(float(rating))
                    self.add_book(book)

    def save_books(self, file_path: str):
        with open(file_path, 'w') as file:
            for book in self.books:
                file.write(book.to_string() + '\n')

    def search_books(self, query: str):
        return [book for book in self.books if query.lower() in book.title.lower()]

    def filter_books(self, criteria: dict):
        filtered_books = self.books
        if 'genre' in criteria:
            filtered_books = [book for book in filtered_books if book.genre == criteria['genre']]
        if 'author' in criteria:
            filtered_books = [book for book in filtered_books if book.author == criteria['author']]
        return filtered_books

    def generate_report(self):
        report = {
            'total_books': len(self.books),
            'average_rating': sum(book.rating for book in self.books) / len(self.books) if self.books else 0
        }
        return report