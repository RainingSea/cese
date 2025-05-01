from typing import List
from book import Book
from file_handler import FileHandler

class BookManager:
    def __init__(self, file_handler: FileHandler) -> None:
        self.file_handler = file_handler
        self.books = self.file_handler.read_books()
        self.shelves = self.file_handler.read_shelves()

    def add_book(self, title: str, author: str, genre: str, year: int, notes: str, rating: float, shelf: str) -> None:
        new_book = Book(title, author, genre, year, [notes], rating, shelf)
        self.books.append(new_book)
        self.file_handler.write_books(self.books)

    def edit_book(self, index: int, title: str, author: str, genre: str, year: int, notes: str, rating: float, shelf: str) -> None:
        if 0 <= index < len(self.books):
            self.books[index] = Book(title, author, genre, year, [notes], rating, shelf)
            self.file_handler.write_books(self.books)

    def delete_book(self, index: int) -> None:
        if 0 <= index < len(self.books):
            del self.books[index]
            self.file_handler.write_books(self.books)

    def search_books(self, query: str) -> List[Book]:
        return [book for book in self.books if query.lower() in book.title.lower() or query.lower() in book.author.lower()]

    def filter_books(self, criteria: str) -> List[Book]:
        return [book for book in self.books if book.genre.lower() == criteria.lower()]

    def filter_books_by_rating(self, min_rating: float) -> List[Book]:
        return [book for book in self.books if book.rating is not None and book.rating >= min_rating]

    def generate_report(self) -> str:
        report = "Book Report:\n"
        for book in self.books:
            report += f"{book.title} by {book.author}, Genre: {book.genre}, Year: {book.publication_year}, Rating: {book.rating}, Shelf: {book.shelf}\n"
        self.file_handler.write_reports([report.strip()])
        return report.strip()

    def create_shelf(self, shelf_name: str) -> None:
        if shelf_name not in self.shelves:
            self.shelves.append(shelf_name)
            self.file_handler.write_shelves(self.shelves)

    def assign_book_to_shelf(self, index: int, shelf: str) -> None:
        if 0 <= index < len(self.books):
            self.books[index].shelf = shelf
            self.file_handler.write_books(self.books)

    def add_note_to_book(self, index: int, note: str) -> None:
        if 0 <= index < len(self.books):
            self.books[index].add_note(note)
            self.file_handler.write_books(self.books)

    def edit_note_in_book(self, index: int, note_index: int, new_note: str) -> None:
        if 0 <= index < len(self.books):
            self.books[index].edit_note(note_index, new_note)
            self.file_handler.write_books(self.books)

    def delete_note_in_book(self, index: int, note_index: int) -> None:
        if 0 <= index < len(self.books):
            self.books[index].delete_note(note_index)
            self.file_handler.write_books(self.books)

    def rate_book(self, book_id: int, rating: float) -> None:
        if 0 <= book_id < len(self.books):
            self.books[book_id].rating = rating
            self.file_handler.write_books(self.books)