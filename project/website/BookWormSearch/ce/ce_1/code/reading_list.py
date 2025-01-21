from data_storage import DataStorage

class ReadingList:
    def __init__(self, user: str):
        self.user = user
        self.data_storage = DataStorage()
        self.books = self.data_storage.load_reading_list(user)

    def add_book(self, book: dict) -> None:
        if book not in self.books:
            self.books.append(book)
            self.data_storage.save_reading_list(self.user, self.books)

    def remove_book(self, book: dict) -> None:
        if book in self.books:
            self.books.remove(book)
            self.data_storage.save_reading_list(self.user, self.books)

    def get_books(self) -> list:
        return self.books