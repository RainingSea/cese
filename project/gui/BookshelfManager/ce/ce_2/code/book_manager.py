from book import Book
from data_handler import DataHandler

class BookManager:
    def __init__(self):
        self.data_handler = DataHandler()
        self.books = self.data_handler.read_books()
        self.notes = self.data_handler.read_notes()
        self.ratings = self.data_handler.read_ratings()
        self.next_id = len(self.books) + 1 if self.books else 1

    def add_book(self, title: str, author: str, genre: str, year: int):
        new_book = Book(self.next_id, title, author, genre, year)
        self.books.append(new_book)
        self.next_id += 1
        self.data_handler.write_books(self.books)

    def add_note(self, book_id: int, note: str):
        self.notes[book_id] = note
        self.data_handler.write_notes(self.notes)

    def add_rating(self, book_id: int, rating: float):
        self.ratings[book_id] = rating
        self.data_handler.write_ratings(self.ratings)

    def generate_report(self):
        report = ""
        for book in self.books:
            report += f"{book.title} by {book.author} - {book.genre} ({book.year})\n"
            report += f"Note: {self.notes.get(book.id, 'No notes')}\n"
            report += f"Rating: {self.ratings.get(book.id, 'No rating')}\n\n"
        return report

    def search_books(self, query: str):
        return [book for book in self.books if query.lower() in book.title.lower()]

    def filter_books(self, criteria: str):
        return [book for book in self.books if book.genre.lower() == criteria.lower()]