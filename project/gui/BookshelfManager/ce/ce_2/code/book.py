class Book:
    def __init__(self, book_id: int, title: str, author: str, genre: str, year: int):
        self.id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.note = ""
        self.rating = 0.0