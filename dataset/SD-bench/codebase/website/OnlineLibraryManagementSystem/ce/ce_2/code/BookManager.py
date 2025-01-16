class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn

    def to_string(self) -> str:
        return f"{self.title}|{self.author}|{self.isbn}"

class BookManager:
    def __init__(self):
        self.books = []

    def load_books(self) -> None:
        try:
            with open('books.txt', 'r') as file:
                for line in file:
                    title, author, isbn = line.strip().split('|')
                    self.add_book(Book(title, author, isbn))
        except FileNotFoundError:
            pass

    def save_books(self) -> None:
        with open('books.txt', 'w') as file:
            for book in self.books:
                file.write(book.to_string() + '\n')

    def add_book(self, book: Book) -> None:
        self.books.append(book)

    def delete_book(self, isbn: str) -> None:
        self.books = [book for book in self.books if book.isbn != isbn]

    def get_books(self) -> list[Book]:
        return self.books