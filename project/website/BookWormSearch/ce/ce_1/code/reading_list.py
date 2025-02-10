class ReadingList:
    def __init__(self, user):
        self.user = user
        self.books = []

    def add_book(self, book) -> bool:
        if book not in self.books:
            self.books.append(book)
            return True
        return False

    def get_books(self) -> list:
        return self.books