import tkinter as tk
from tkinter import messagebox, simpledialog, Listbox, Scrollbar
from typing import List

class Book:
    def __init__(self, title: str, author: str, genre: str, publication_date: str):
        self.title = title
        self.author = author
        self.genre = genre
        self.publication_date = publication_date

    def save(self):
        with open('books.txt', 'a') as file:
            file.write(f"{self.title}|{self.author}|{self.genre}|{self.publication_date}\n")

class Note:
    def __init__(self, book_title: str, chapter: str, content: str):
        self.book_title = book_title
        self.chapter = chapter
        self.content = content

    def save(self):
        with open('notes.txt', 'a') as file:
            file.write(f"{self.book_title}|{self.chapter}|{self.content}\n")

class BookManager:
    def add_book(self, book: Book):
        book.save()

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

    def search_books(self, query: str) -> List[Book]:
        return [book for book in self.load_books() if query.lower() in book.title.lower()]

class NoteManager:
    def add_note(self, note: Note):
        note.save()

    def load_notes(self) -> List[Note]:
        notes = []
        try:
            with open('notes.txt', 'r') as file:
                for line in file:
                    book_title, chapter, content = line.strip().split('|')
                    notes.append(Note(book_title, chapter, content))
        except FileNotFoundError:
            pass
        return notes

    def search_notes(self, query: str) -> List[Note]:
        return [note for note in self.load_notes() if query.lower() in note.content.lower()]

class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("BookNote Application")
        self.book_manager = BookManager()
        self.note_manager = NoteManager()

        self.create_widgets()

    def create_widgets(self):
        # Book input
        tk.Label(self.master, text="Title").grid(row=0, column=0)
        self.title_entry = tk.Entry(self.master)
        self.title_entry.grid(row=0, column=1)

        tk.Label(self.master, text="Author").grid(row=1, column=0)
        self.author_entry = tk.Entry(self.master)
        self.author_entry.grid(row=1, column=1)

        tk.Label(self.master, text="Genre").grid(row=2, column=0)
        self.genre_entry = tk.Entry(self.master)
        self.genre_entry.grid(row=2, column=1)

        tk.Label(self.master, text="Publication Date").grid(row=3, column=0)
        self.pub_date_entry = tk.Entry(self.master)
        self.pub_date_entry.grid(row=3, column=1)

        tk.Button(self.master, text="Add Book", command=self.add_book_ui).grid(row=4, columnspan=2)

        # Notes input
        tk.Label(self.master, text="Book Title").grid(row=5, column=0)
        self.note_title_entry = tk.Entry(self.master)
        self.note_title_entry.grid(row=5, column=1)

        tk.Label(self.master, text="Chapter").grid(row=6, column=0)
        self.chapter_entry = tk.Entry(self.master)
        self.chapter_entry.grid(row=6, column=1)

        tk.Label(self.master, text="Note Content").grid(row=7, column=0)
        self.note_content_entry = tk.Text(self.master, height=5, width=20)
        self.note_content_entry.grid(row=7, column=1)

        tk.Button(self.master, text="Add Note", command=self.add_note_ui).grid(row=8, columnspan=2)

        # Search
        tk.Label(self.master, text="Search Books").grid(row=9, column=0)
        self.search_entry = tk.Entry(self.master)
        self.search_entry.grid(row=9, column=1)
        tk.Button(self.master, text="Search", command=self.search_books_ui).grid(row=10, columnspan=2)

        tk.Label(self.master, text="Search Notes").grid(row=11, column=0)
        self.search_note_entry = tk.Entry(self.master)
        self.search_note_entry.grid(row=11, column=1)
        tk.Button(self.master, text="Search", command=self.search_notes_ui).grid(row=12, columnspan=2)

        # Listbox for displaying results
        self.result_listbox = Listbox(self.master)
        self.result_listbox.grid(row=13, columnspan=2)

    def add_book_ui(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        publication_date = self.pub_date_entry.get()
        if title and author and genre and publication_date:
            book = Book(title, author, genre, publication_date)
            self.book_manager.add_book(book)
            messagebox.showinfo("Success", "Book added successfully!")
        else:
            messagebox.showwarning("Input Error", "All fields must be filled.")

    def add_note_ui(self):
        book_title = self.note_title_entry.get()
        chapter = self.chapter_entry.get()
        content = self.note_content_entry.get("1.0", tk.END).strip()
        if book_title and chapter and content:
            note = Note(book_title, chapter, content)
            self.note_manager.add_note(note)
            messagebox.showinfo("Success", "Note added successfully!")
        else:
            messagebox.showwarning("Input Error", "All fields must be filled.")

    def search_books_ui(self):
        query = self.search_entry.get()
        results = self.book_manager.search_books(query)
        self.result_listbox.delete(0, tk.END)
        for book in results:
            self.result_listbox.insert(tk.END, f"{book.title} by {book.author}")

    def search_notes_ui(self):
        query = self.search_note_entry.get()
        results = self.note_manager.search_notes(query)
        self.result_listbox.delete(0, tk.END)
        for note in results:
            self.result_listbox.insert(tk.END, f"{note.book_title} - {note.chapter}: {note.content}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()