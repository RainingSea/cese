import os
from .Book import Book

class BookManager:
    def __init__(self) -> None:
        self.books = {}

    def add_book(self, title: str, author: str, genre: str, pub_date: str) -> None:
        if title not in self.books:
            self.books[title] = Book(title, author, genre, pub_date)
            self.save_books()

    def add_note_to_chapter(self, title: str, chapter: int, note: str) -> None:
        if title in self.books:
            self.books[title].add_chapter_note(chapter, note)
            self.save_books()

    def search_books(self, query: str) -> list:
        return [book for book in self.books.keys() if query.lower() in book.lower()]

    def search_notes(self, query: str) -> list:
        results = []
        for book in self.books.values():
            for chapter, notes in book.get_notes().items():
                for note in notes:
                    if query.lower() in note.lower():
                        results.append((book.title, chapter, note))
        return results

    def load_books(self) -> None:
        for filename in os.listdir('books/'):
            if filename.endswith('.txt'):
                with open(os.path.join('books/', filename), 'r') as file:
                    title = filename[:-4].replace('_', ' ')
                    self.books[title] = Book(title, "", "", "")
                    for line in file:
                        if line.startswith('Chapter'):
                            chapter, note = line.split(':', 1)
                            chapter_number = int(chapter.split()[1])
                            self.books[title].add_chapter_note(chapter_number, note.strip())

    def save_books(self) -> None:
        for title, book in self.books.items():
            with open(os.path.join('books/', f"{title.replace(' ', '_')}.txt"), 'w') as file:
                for chapter, notes in book.get_notes().items():
                    for note in notes:
                        file.write(f"Chapter {chapter}: {note}\n")