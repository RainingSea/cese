class ReadingList:
    def __init__(self, user):
        self.user = user
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, book):
        self.books.remove(book)

    def view_list(self):
        return self.books