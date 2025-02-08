import tkinter as tk
from tkinter import messagebox, simpledialog
from typing import List

class Book:
    def __init__(self, title: str, author: str, genre: str, publication_date: str):
        self.title = title
        self.author = author
        self.genre = genre
        self.publication_date = publication_date

    def to_string(self) -> str:
        return f"{self.title}|{self.author}|{self.genre}|{self.publication_date}"

class Note:
    def __init__(self, book_title: str, chapter: str, note_text: str):
        self.book_title = book_title
        self.chapter = chapter
        self.note_text = note_text

    def to_string(self) -> str:
        return f"{self.book_title}|{self.chapter}|{self.note_text}"

class BookManager:
    def __init__(self):
        self.books: List[Book] = self.load_books()

    def add_book(self, book: Book):
        self.books.append(book)
        self.save_books()

    def load_books(self) -> List[Book]:
        books = []
        try:
            with open('books.txt', 'r') as file:
                for line in file:
                    title, author, genre, publication_date = line.strip().split('|')
                    books.append(Book(title, author, genre, publication_date))
        except FileNotFoundError:
            pass
        return books

    def save_books(self):
        with open('books.txt', 'w') as file:
            for book in self.books:
                file.write(book.to_string() + '\n')

    def search_books(self, query: str) -> List[Book]:
        return [book for book in self.books if query.lower() in book.title.lower()]

class NoteManager:
    def __init__(self):
        self.notes: List[Note] = self.load_notes()

    def add_note(self, note: Note):
        self.notes.append(note)
        self.save_notes()

    def load_notes(self) -> List[Note]:
        notes = []
        try:
            with open('notes.txt', 'r') as file:
                for line in file:
                    book_title, chapter, note_text = line.strip().split('|')
                    notes.append(Note(book_title, chapter, note_text))
        except FileNotFoundError:
            pass
        return notes

    def save_notes(self):
        with open('notes.txt', 'w') as file:
            for note in self.notes:
                file.write(note.to_string() + '\n')

    def search_notes(self, query: str) -> List[Note]:
        return [note for note in self.notes if query.lower() in note.note_text.lower()]

class MainApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("BookNote Application")
        self.book_manager = BookManager()
        self.note_manager = NoteManager()

        self.create_widgets()

    def create_widgets(self):
        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()
        self.author_entry = tk.Entry(self.root)
        self.author_entry.pack()
        self.genre_entry = tk.Entry(self.root)
        self.genre_entry.pack()
        self.pub_date_entry = tk.Entry(self.root)
        self.pub_date_entry.pack()

        self.add_book_button = tk.Button(self.root, text="Add Book", command=self.add_book)
        self.add_book_button.pack()

        self.book_listbox = tk.Listbox(self.root)
        self.book_listbox.pack()
        self.book_listbox.bind('<<ListboxSelect>>', self.on_book_select)

        self.note_text = tk.Text(self.root)
        self.note_text.pack()

        self.add_note_button = tk.Button(self.root, text="Add Note", command=self.add_note)
        self.add_note_button.pack()

        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack()
        self.search_button = tk.Button(self.root, text="Search Books", command=self.search_books)
        self.search_button.pack()

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        publication_date = self.pub_date_entry.get()
        book = Book(title, author, genre, publication_date)
        self.book_manager.add_book(book)
        self.update_book_list()

    def add_note(self):
        selected_book = self.book_listbox.get(tk.ACTIVE)
        chapter = simpledialog.askstring("Input", "Enter chapter:")
        note_text = self.note_text.get("1.0", tk.END).strip()
        if selected_book and chapter and note_text:
            note = Note(selected_book, chapter, note_text)
            self.note_manager.add_note(note)

    def on_book_select(self, event):
        selected_book = self.book_listbox.get(tk.ACTIVE)
        self.note_text.delete("1.0", tk.END)
        for note in self.note_manager.notes:
            if note.book_title == selected_book:
                self.note_text.insert(tk.END, f"{note.chapter}: {note.note_text}\n")

    def search_books(self):
        query = self.search_entry.get()
        found_books = self.book_manager.search_books(query)
        self.book_listbox.delete(0, tk.END)
        for book in found_books:
            self.book_listbox.insert(tk.END, book.title)

    def update_book_list(self):
        self.book_listbox.delete(0, tk.END)
        for book in self.book_manager.books:
            self.book_listbox.insert(tk.END, book.title)

    def run(self):
        self.update_book_list()
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    app.run()