from user import User
from book import Book

class ReadingList:
    def __init__(self):
        self.user = User()
        self.books = self.load_reading_list()

    def load_reading_list(self) -> list:
        reading_list = []
        with open('reading_list.txt', 'r') as file:
            for line in file:
                title, author, summary = line.strip().split('|')
                reading_list.append(Book(title, author, summary))
        return reading_list

    def remove_book(self, book: Book) -> bool:
        # Placeholder for removing book logic
        return True