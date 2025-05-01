import os

class DataHandler:
    def __init__(self):
        self.books_file = 'books.txt'
        self.notes_file = 'notes.txt'
        self.ratings_file = 'ratings.txt'

    def read_books(self):
        if not os.path.exists(self.books_file):
            return []
        with open(self.books_file, 'r') as file:
            lines = file.readlines()
            books = []
            for line in lines:
                parts = line.strip().split('|')
                book_id = int(parts[0])
                title = parts[1]
                author = parts[2]
                genre = parts[3]
                year = int(parts[4])
                books.append(Book(book_id, title, author, genre, year))
            return books

    def write_books(self, books):
        with open(self.books_file, 'w') as file:
            for book in books:
                file.write(f"{book.id}|{book.title}|{book.author}|{book.genre}|{book.year}\n")

    def read_notes(self):
        if not os.path.exists(self.notes_file):
            return {}
        with open(self.notes_file, 'r') as file:
            lines = file.readlines()
            notes = {}
            for line in lines:
                parts = line.strip().split('|')
                notes[int(parts[0])] = parts[1]
            return notes

    def write_notes(self, notes):
        with open(self.notes_file, 'w') as file:
            for book_id, note in notes.items():
                file.write(f"{book_id}|{note}\n")

    def read_ratings(self):
        if not os.path.exists(self.ratings_file):
            return {}
        with open(self.ratings_file, 'r') as file:
            lines = file.readlines()
            ratings = {}
            for line in lines:
                parts = line.strip().split('|')
                ratings[int(parts[0])] = float(parts[1])
            return ratings

    def write_ratings(self, ratings):
        with open(self.ratings_file, 'w') as file:
            for book_id, rating in ratings.items():
                file.write(f"{book_id}|{rating}\n")