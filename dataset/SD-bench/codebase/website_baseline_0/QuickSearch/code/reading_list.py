class ReadingList:
    def __init__(self, user: str):
        self.user = user
        self.books = []

    def add_book(self, book: 'Book') -> None:
        self.books.append(book)

    def get_books(self) -> list:
        return self.books