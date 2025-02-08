class Book:
    def __init__(self, title: str, author: str, genre: str, publication_date: str):
        self.title = title
        self.author = author
        self.genre = genre
        self.publication_date = publication_date

class Note:
    def __init__(self, book_title: str, chapter: str, text: str):
        self.book_title = book_title
        self.chapter = chapter
        self.text = text