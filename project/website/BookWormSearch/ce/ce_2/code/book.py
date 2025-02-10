class Book:
    def __init__(self, title: str, author: str, summary: str):
        self.title = title
        self.author = author
        self.summary = summary

    @staticmethod
    def load_books() -> list:
        books = []
        try:
            with open('books.txt', 'r') as f:
                for line in f:
                    title, author, summary = line.strip().split('|')
                    books.append(Book(title, author, summary))
        except FileNotFoundError:
            pass
        return books