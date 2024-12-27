class Book:
    def __init__(self, title: str, author: str, content: str):
        self.title = title
        self.author = author
        self.content = content

    def save(self):
        with open('books.txt', 'a') as file:
            file.write(f"{self.title}|{self.author}|{self.content}\n")

class BookManager:
    def __init__(self, books_file: str):
        self.books_file = books_file

    def create_book(self, title: str, author: str, content: str) -> None:
        book = Book(title, author, content)
        book.save()

    def load_books(self) -> list:
        books = []
        try:
            with open(self.books_file, 'r') as file:
                for line in file:
                    title, author, content = line.strip().split('|')
                    books.append(Book(title, author, content))
        except FileNotFoundError:
            pass
        return books

    def get_book_details(self, title: str) -> Book:
        books = self.load_books()
        for book in books:
            if book.title == title:
                return book
        return None