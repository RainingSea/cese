import json

class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn

    def to_dict(self) -> dict:
        return {"title": self.title, "author": self.author, "isbn": self.isbn}

class BookManager:
    def __init__(self):
        self.books = []
        self.file_path = 'books.txt'
        self.load_books()

    def load_books(self) -> None:
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    title, author, isbn = line.strip().split('|')
                    self.add_book(Book(title, author, isbn))
        except FileNotFoundError:
            print("Warning: books.txt not found. Starting with an empty book list.")

    def save_books(self) -> None:
        with open(self.file_path, 'w') as file:
            for book in self.books:
                file.write(f"{book.title}|{book.author}|{book.isbn}\n")

    def add_book(self, book: Book) -> bool:
        if any(existing_book.title == book.title for existing_book in self.books):
            return False
        self.books.append(book)
        self.save_books()
        return True

    def delete_book(self, isbn: str) -> None:
        self.books = [book for book in self.books if book.isbn != isbn]
        self.save_books()

    def get_books(self) -> list:
        return self.books

    def search_books(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book.title.lower() or query.lower() in book.author.lower()]