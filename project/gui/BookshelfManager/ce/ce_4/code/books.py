class Book:
    def __init__(self, title: str, author: str, genre: str, year: int, notes: str, rating: float) -> None:
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.notes = notes
        self.rating = rating


class BookManager:
    def __init__(self):
        self.books = []

    def add_book(self, title: str, author: str, genre: str, year: int, notes: str, rating: float) -> None:
        new_book = Book(title, author, genre, year, notes, rating)
        self.books.append(new_book)

    def search_books(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book.title.lower() or query.lower() in book.author.lower()]

    def filter_books(self, criteria: dict) -> list:
        filtered_books = self.books
        if 'genre' in criteria:
            filtered_books = [book for book in filtered_books if book.genre == criteria['genre']]
        if 'year' in criteria:
            filtered_books = [book for book in filtered_books if book.year == criteria['year']]
        return filtered_books

    def generate_report(self) -> str:
        report_lines = [f"{book.title} by {book.author} - {book.genre} ({book.year}) - Rating: {book.rating}\nNotes: {book.notes}" for book in self.books]
        return "\n".join(report_lines)

    def load_books(self) -> None:
        from data_management import load_books_from_file
        self.books = load_books_from_file()

    def save_books(self) -> None:
        from data_management import save_books_to_file
        save_books_to_file(self.books)