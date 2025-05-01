import os

class DataManager:
    def __init__(self):
        self.books_file = 'books.txt'
        self.notes_file = 'notes.txt'
        self.categories_file = 'categories.txt'

    def load_books(self):
        if not os.path.exists(self.books_file):
            return []
        with open(self.books_file, 'r') as file:
            return [line.strip() for line in file.readlines()]

    def save_book(self, title: str, author: str, pub_date: str):
        with open(self.books_file, 'a') as file:
            file.write(f"{title}|{author}|{pub_date}\n")

    def load_notes(self):
        if not os.path.exists(self.notes_file):
            return []
        with open(self.notes_file, 'r') as file:
            return [line.strip() for line in file.readlines()]

    def save_note(self, book_id: int, chapter: str, note: str):
        with open(self.notes_file, 'a') as file:
            file.write(f"{book_id}|{chapter}|{note}\n")

    def load_categories(self):
        if not os.path.exists(self.categories_file):
            return []
        with open(self.categories_file, 'r') as file:
            return [line.strip() for line in file.readlines()]

    def save_category(self, category: str):
        with open(self.categories_file, 'a') as file:
            file.write(f"{category}\n")