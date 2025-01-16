class Book:
    def __init__(self, title: str, author: str, summary: str, cover_image: str):
        self.title = title
        self.author = author
        self.summary = summary
        self.cover_image = cover_image

    @staticmethod
    def load_books() -> list:
        books = []
        with open('books.txt', 'r') as file:
            for line in file:
                title, author, summary, cover_image = line.strip().split('|')
                books.append(Book(title, author, summary, cover_image))
        return books