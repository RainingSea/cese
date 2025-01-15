class Book:
    def __init__(self, title: str, author: str, summary: str):
        self.title = title
        self.author = author
        self.summary = summary

    @staticmethod
    def load_all() -> list:
        books = []
        try:
            with open('books.txt', 'r') as file:
                for line in file:
                    title, author, summary = line.strip().split('|')
                    books.append(Book(title, author, summary))
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return books