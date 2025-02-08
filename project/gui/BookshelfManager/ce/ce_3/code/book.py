class Book:
    def __init__(self, title: str, author: str, genre: str, publication_year: int):
        self.title = title
        self.author = author
        self.genre = genre
        self.publication_year = publication_year
        self.notes = ""
        self.rating = 0.0

    def add_notes(self, notes: str):
        self.notes = notes

    def add_rating(self, rating: float):
        if 0 <= rating <= 5:
            self.rating = rating

    def to_string(self) -> str:
        return f"{self.title},{self.author},{self.genre},{self.publication_year},{self.notes},{self.rating}"