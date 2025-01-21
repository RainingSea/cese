class Book:
    def __init__(self, title: str, author: str, summary: str):
        self.title = title
        self.author = author
        self.summary = summary

    def save(self) -> None:
        """Save the book to the books.txt file."""
        with open('books.txt', 'a') as file:
            file.write(f"{self.title}|{self.author}|{self.summary}\n")

    @staticmethod
    def load_all() -> list:
        """Load all books from the books.txt file."""
        books = []
        with open('books.txt', 'r') as file:
            for line in file:
                title, author, summary = line.strip().split('|')
                books.append(Book(title, author, summary))
        return books