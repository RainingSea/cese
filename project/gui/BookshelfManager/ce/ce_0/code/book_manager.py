import os

class BookManager:
    def __init__(self):
        self.books = []
        self.shelves = []

    def add_book(self, title: str, author: str, genre: str, year: int, notes: str, rating: float, shelf: str) -> None:
        book_entry = f"{title}|{author}|{genre}|{year}|{notes}|{rating}|{shelf}"
        self.books.append(book_entry)
        self.save_data()

    def generate_report(self) -> str:
        report = "Books in Collection:\n"
        for book in self.books:
            report += f"{book}\n"
        return report.strip()

    def search_books(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book.lower()]

    def filter_books(self, criteria: str) -> list:
        return [book for book in self.books if criteria.lower() in book.lower()]

    def load_data(self) -> None:
        if os.path.exists("books.txt"):
            with open("books.txt", "r") as file:
                self.books = [line.strip() for line in file.readlines()]
        if os.path.exists("shelves.txt"):
            with open("shelves.txt", "r") as file:
                self.shelves = [line.strip() for line in file.readlines()]

    def save_data(self) -> None:
        with open("books.txt", "w") as file:
            for book in self.books:
                file.write(book + "\n")
        with open("shelves.txt", "w") as file:
            for shelf in self.shelves:
                file.write(shelf + "\n")