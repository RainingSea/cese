import tkinter as tk
from tkinter import messagebox
from typing import List

class Book:
    def __init__(self, title: str, author: str, publication_date: str):
        self.title = title
        self.author = author
        self.publication_date = publication_date

class Note:
    def __init__(self, chapter: str, content: str):
        self.chapter = chapter
        self.content = content

class BookManager:
    def __init__(self):
        self.books: List[Book] = []
        self.load_books()

    def add_book(self, title: str, author: str, publication_date: str) -> None:
        new_book = Book(title, author, publication_date)
        self.books.append(new_book)
        self.save_books()

    def load_books(self) -> None:
        try:
            with open('books.txt', 'r') as file:
                for line in file:
                    title, author, publication_date = line.strip().split('|')
                    self.books.append(Book(title, author, publication_date))
        except FileNotFoundError:
            pass

    def save_books(self) -> None:
        with open('books.txt', 'w') as file:
            for book in self.books:
                file.write(f"{book.title}|{book.author}|{book.publication_date}\n")

class NoteManager:
    def __init__(self):
        self.notes: List[Note] = []
        self.load_notes()

    def add_note(self, chapter: str, content: str) -> None:
        new_note = Note(chapter, content)
        self.notes.append(new_note)
        self.save_notes()

    def load_notes(self) -> None:
        try:
            with open('notes.txt', 'r') as file:
                for line in file:
                    chapter, content = line.strip().split('|')
                    self.notes.append(Note(chapter, content))
        except FileNotFoundError:
            pass

    def save_notes(self) -> None:
        with open('notes.txt', 'w') as file:
            for note in self.notes:
                file.write(f"{note.chapter}|{note.content}\n")

class SearchEngine:
    def search_books(self, query: str, book_manager: BookManager) -> List[Book]:
        return [book for book in book_manager.books if query.lower() in book.title.lower()]

    def search_notes(self, query: str, note_manager: NoteManager) -> List[Note]:
        return [note for note in note_manager.notes if query.lower() in note.content.lower()]

class Main:
    def __init__(self):
        self.book_manager = BookManager()
        self.note_manager = NoteManager()
        self.search_engine = SearchEngine()
        self.setup_ui()

    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("BookNote Application")

        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()
        self.author_entry = tk.Entry(self.root)
        self.author_entry.pack()
        self.pub_date_entry = tk.Entry(self.root)
        self.pub_date_entry.pack()
        self.add_book_button = tk.Button(self.root, text="Add Book", command=self.add_book)
        self.add_book_button.pack()

        self.chapter_entry = tk.Entry(self.root)
        self.chapter_entry.pack()
        self.note_entry = tk.Entry(self.root)
        self.note_entry.pack()
        self.add_note_button = tk.Button(self.root, text="Add Note", command=self.add_note)
        self.add_note_button.pack()

        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack()
        self.search_button = tk.Button(self.root, text="Search Books", command=self.search_books)
        self.search_button.pack()

        self.root.mainloop()

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        publication_date = self.pub_date_entry.get()
        self.book_manager.add_book(title, author, publication_date)
        messagebox.showinfo("Success", "Book added successfully!")

    def add_note(self):
        chapter = self.chapter_entry.get()
        content = self.note_entry.get()
        self.note_manager.add_note(chapter, content)
        messagebox.showinfo("Success", "Note added successfully!")

    def search_books(self):
        query = self.search_entry.get()
        results = self.search_engine.search_books(query, self.book_manager)
        result_titles = "\n".join(book.title for book in results)
        messagebox.showinfo("Search Results", result_titles if result_titles else "No books found.")

def main():
    app = Main()

if __name__ == "__main__":
    main()