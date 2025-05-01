import os
from typing import List
from book import Book

class FileHandler:
    def __init__(self, books_file: str, shelves_file: str, reports_file: str) -> None:
        self.books_file = books_file
        self.shelves_file = shelves_file
        self.reports_file = reports_file

    def read_books(self) -> List[Book]:
        books = []
        if os.path.exists(self.books_file):
            with open(self.books_file, 'r') as file:
                for line in file:
                    title, author, genre, year, notes, rating, shelf = line.strip().split('|')
                    notes_list = notes.split(';') if notes else []
                    books.append(Book(title, author, genre, int(year), notes_list, float(rating) if rating else None, shelf))
        return books

    def write_books(self, books: List[Book]) -> None:
        with open(self.books_file, 'w') as file:
            for book in books:
                notes_str = ';'.join(book.notes)
                file.write(f"{book.title}|{book.author}|{book.genre}|{book.publication_year}|{notes_str}|{book.rating if book.rating is not None else ''}|{book.shelf}\n")

    def read_shelves(self) -> List[str]:
        if os.path.exists(self.shelves_file):
            with open(self.shelves_file, 'r') as file:
                return [line.strip() for line in file]
        return []

    def write_shelves(self, shelves: List[str]) -> None:
        with open(self.shelves_file, 'w') as file:
            for shelf in shelves:
                file.write(f"{shelf}\n")

    def read_reports(self) -> List[str]:
        if os.path.exists(self.reports_file):
            with open(self.reports_file, 'r') as file:
                return [line.strip() for line in file]
        return []

    def write_reports(self, reports: List[str]) -> None:
        with open(self.reports_file, 'w') as file:
            for report in reports:
                file.write(f"{report}\n")