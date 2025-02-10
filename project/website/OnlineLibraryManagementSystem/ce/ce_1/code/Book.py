class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn

    def save(self) -> None:
        with open('books.txt', 'a') as file:
            file.write(f"{self.title}|{self.author}|{self.isbn}\n")

    @staticmethod
    def load_books() -> list:
        books = []
        try:
            with open('books.txt', 'r') as file:
                for line in file:
                    title, author, isbn = line.strip().split('|')
                    books.append(Book(title, author, isbn))
        except FileNotFoundError:
            pass
        return books