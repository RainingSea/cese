import os
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("BookNote Application")
        self.book_manager = BookManager()
        self.note_manager = NoteManager()
        self.create_ui()

    def create_ui(self):
        # Input fields for book details
        tk.Label(self.root, text="Title").grid(row=0, column=0)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Author").grid(row=1, column=0)
        self.author_entry = tk.Entry(self.root)
        self.author_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Publication Date").grid(row=2, column=0)
        self.pub_date_entry = tk.Entry(self.root)
        self.pub_date_entry.grid(row=2, column=1)

        tk.Button(self.root, text="Save Book", command=self.save_book).grid(row=3, columnspan=2)

        # Text area for notes
        tk.Label(self.root, text="Chapter").grid(row=4, column=0)
        self.chapter_entry = tk.Entry(self.root)
        self.chapter_entry.grid(row=4, column=1)

        tk.Label(self.root, text="Note").grid(row=5, column=0)
        self.note_text = scrolledtext.ScrolledText(self.root, width=40, height=10)
        self.note_text.grid(row=5, column=1)

        tk.Button(self.root, text="Add Note", command=self.add_note).grid(row=6, columnspan=2)

        tk.Button(self.root, text="Search Notes", command=self.search_notes).grid(row=7, columnspan=2)

    def save_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        pub_date = self.pub_date_entry.get()
        if title and author and pub_date:
            self.book_manager.add_book(title, author, pub_date)
            messagebox.showinfo("Info", "Book saved successfully!")
        else:
            messagebox.showwarning("Warning", "Please fill all fields.")

    def add_note(self):
        book_title = self.title_entry.get()
        chapter = self.chapter_entry.get()
        content = self.note_text.get("1.0", tk.END).strip()
        if book_title and chapter and content:
            self.note_manager.add_note(book_title, chapter, content)
            messagebox.showinfo("Info", "Note added successfully!")
        else:
            messagebox.showwarning("Warning", "Please fill all fields.")

    def search_notes(self):
        query = simpledialog.askstring("Search Notes", "Enter search query:")
        if query:
            results = self.note_manager.search_notes(query)
            if results:
                messagebox.showinfo("Search Results", "\n".join(results))
            else:
                messagebox.showinfo("Search Results", "No notes found.")

class BookManager:
    def __init__(self):
        self.books = self.load_books()

    def add_book(self, title: str, author: str, pub_date: str):
        with open("books.txt", "a") as file:
            file.write(f"{title}|{author}|{pub_date}\n")
        self.books.append((title, author, pub_date))

    def load_books(self) -> list:
        if not os.path.exists("books.txt"):
            return []
        with open("books.txt", "r") as file:
            return [tuple(line.strip().split("|")) for line in file.readlines()]

class NoteManager:
    def __init__(self):
        self.notes = self.load_notes()

    def add_note(self, book_title: str, chapter: str, content: str):
        with open("notes.txt", "a") as file:
            file.write(f"{book_title}|{chapter}|{content}\n")
        self.notes.append((book_title, chapter, content))

    def load_notes(self) -> list:
        if not os.path.exists("notes.txt"):
            return []
        with open("notes.txt", "r") as file:
            return [tuple(line.strip().split("|")) for line in file.readlines()]

    def search_notes(self, query: str) -> list:
        return [f"{book_title} - {chapter}: {content}" for book_title, chapter, content in self.notes if query in content]

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()