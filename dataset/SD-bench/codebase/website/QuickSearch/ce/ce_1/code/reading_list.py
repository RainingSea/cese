class ReadingList:
    def __init__(self, user):
        self.user = user
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def get_books(self) -> list:
        return self.books