class Book:
    def __init__(self, title: str, author: str, content: str):
        self.title = title
        self.author = author
        self.content = content

    def save(self):
        with open('books.txt', 'a') as f:
            f.write(f"{self.title}|{self.author}|{self.content}\n")

class BookManager:
    def __init__(self):
        self.books = []

    def load_books(self):
        try:
            with open('books.txt', 'r') as f:
                for line in f:
                    title, author, content = line.strip().split('|')
                    self.books.append(Book(title, author, content))
        except FileNotFoundError:
            pass

    def add_book(self, title: str, author: str, content: str) -> None:
        new_book = Book(title, author, content)
        new_book.save()
        self.books.append(new_book)

    def get_books(self) -> list:
        return self.books

    def get_book_details(self, title: str) -> Book:
        for book in self.books:
            if book.title == title:
                return book
        return None