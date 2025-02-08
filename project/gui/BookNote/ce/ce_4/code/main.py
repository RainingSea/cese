import tkinter as tk
from tkinter import messagebox
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
    def __init__(self, book_title: str, chapter: str, content: str):
        self.book_title = book_title
        self.chapter = chapter
        self.content = content

    def to_string(self) -> str:
        return f"{self.book_title}|{self.chapter}|{self.content}"

class BookNoteApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("BookNote Application")
        self.books: List[Book] = []
        self.notes: List[Note] = []
        self.load_data()
        self.create_widgets()

    def create_widgets(self):
        # Book input fields
        tk.Label(self.root, text="Title").grid(row=0, column=0)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Author").grid(row=1, column=0)
        self.author_entry = tk.Entry(self.root)
        self.author_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Genre").grid(row=2, column=0)
        self.genre_entry = tk.Entry(self.root)
        self.genre_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Publication Date").grid(row=3, column=0)
        self.pub_date_entry = tk.Entry(self.root)
        self.pub_date_entry.grid(row=3, column=1)

        tk.Button(self.root, text="Add Book", command=self.add_book).grid(row=4, column=0, columnspan=2)

        # Notes input fields
        tk.Label(self.root, text="Book Title for Note").grid(row=5, column=0)
        self.note_title_entry = tk.Entry(self.root)
        self.note_title_entry.grid(row=5, column=1)

        tk.Label(self.root, text="Chapter").grid(row=6, column=0)
        self.chapter_entry = tk.Entry(self.root)
        self.chapter_entry.grid(row=6, column=1)

        tk.Label(self.root, text="Note Content").grid(row=7, column=0)
        self.note_content_entry = tk.Entry(self.root)
        self.note_content_entry.grid(row=7, column=1)

        tk.Button(self.root, text="Add Note", command=self.add_note).grid(row=8, column=0, columnspan=2)

        # Search bar
        tk.Label(self.root, text="Search Books/Notes").grid(row=9, column=0)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=9, column=1)
        tk.Button(self.root, text="Search", command=self.search).grid(row=10, column=0, columnspan=2)

        # Display area
        self.display_area = tk.Text(self.root, height=10, width=50)
        self.display_area.grid(row=11, column=0, columnspan=2)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        publication_date = self.pub_date_entry.get()
        if title and author and genre and publication_date:
            new_book = Book(title, author, genre, publication_date)
            self.books.append(new_book)
            self.save_data()
            messagebox.showinfo("Success", "Book added successfully!")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")

    def add_note(self):
        book_title = self.note_title_entry.get()
        chapter = self.chapter_entry.get()
        content = self.note_content_entry.get()
        if book_title and chapter and content:
            new_note = Note(book_title, chapter, content)
            self.notes.append(new_note)
            self.save_data()
            messagebox.showinfo("Success", "Note added successfully!")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")

    def search(self):
        query = self.search_entry.get()
        results = []
        for book in self.books:
            if query.lower() in book.title.lower() or query.lower() in book.author.lower():
                results.append(book.to_string())
        for note in self.notes:
            if query.lower() in note.book_title.lower() or query.lower() in note.content.lower():
                results.append(note.to_string())
        self.display_area.delete(1.0, tk.END)
        self.display_area.insert(tk.END, "\n".join(results) if results else "No results found.")

    def load_data(self):
        try:
            with open('books.txt', 'r') as book_file:
                for line in book_file:
                    title, author, genre, publication_date = line.strip().split('|')
                    self.books.append(Book(title, author, genre, publication_date))
            with open('notes.txt', 'r') as note_file:
                for line in note_file:
                    book_title, chapter, content = line.strip().split('|')
                    self.notes.append(Note(book_title, chapter, content))
        except FileNotFoundError:
            pass

    def save_data(self):
        with open('books.txt', 'w') as book_file:
            for book in self.books:
                book_file.write(book.to_string() + '\n')
        with open('notes.txt', 'w') as note_file:
            for note in self.notes:
                note_file.write(note.to_string() + '\n')

if __name__ == "__main__":
    root = tk.Tk()
    app = BookNoteApp(root)
    root.mainloop()