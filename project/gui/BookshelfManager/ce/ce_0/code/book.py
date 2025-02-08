class Book:
    def __init__(self, title: str, author: str, genre: str, year: int, shelf: str, notes: str, rating: float):
        self.title = title
        self.author = author
        self.genre = genre
        self.publication_year = year
        self.shelf = shelf
        self.notes = notes
        self.rating = rating