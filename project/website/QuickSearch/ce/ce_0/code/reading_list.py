import os
from user import User
from book import Book

class ReadingList:
    reading_list_file = 'reading_list.txt'

    def __init__(self, user: str):
        self.user = user
        self.books = self.load_reading_list()

    def load_reading_list(self):
        reading_list = []
        if os.path.exists(self.reading_list_file):
            with open(self.reading_list_file, 'r') as file:
                for line in file:
                    username, title = line.strip().split('|')
                    if username == self.user:
                        reading_list.append(title)
        return reading_list

    def add_book(self, book: Book):
        if book.title not in self.books:
            with open(self.reading_list_file, 'a') as file:
                file.write(f"{self.user}|{book.title}\n")
            self.books.append(book.title)
            return True
        return False

    def remove_book(self, book: Book):
        if book.title in self.books:
            self.books.remove(book.title)
            self.save_reading_list()
            return True
        return False

    def get_books(self):
        return self.books

    def save_reading_list(self):
        with open(self.reading_list_file, 'w') as file:
            for title in self.books:
                file.write(f"{self.user}|{title}\n")