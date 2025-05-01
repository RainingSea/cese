class Book:
    def __init__(self, title: str, author: str, publication_date: str):
        self.title = title
        self.author = author
        self.publication_date = publication_date

class BookManager:
    def __init__(self):
        self.books = []
        self.load_books()

    def add_book(self, title: str, author: str, pub_date: str):
        new_book = Book(title, author, pub_date)
        self.books.append(new_book)
        self.save_books()

    def load_books(self) -> None:
        try:
            with open("books.txt", "r") as file:
                for line in file:
                    title, author, pub_date = line.strip().split("|")
                    self.books.append(Book(title, author, pub_date))
        except FileNotFoundError:
            pass

    def save_books(self) -> None:
        with open("books.txt", "w") as file:
            for book in self.books:
                file.write(f"{book.title}|{book.author}|{book.publication_date}\n")