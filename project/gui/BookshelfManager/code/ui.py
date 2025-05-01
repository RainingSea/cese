import tkinter as tk
from tkinter import messagebox, Listbox, Entry, Button, StringVar
from book_manager import BookManager

class UI:
    def __init__(self, root: tk.Tk, book_manager: BookManager) -> None:
        self.root = root
        self.book_manager = book_manager
        self.root.title("Bookshelf Manager")

        self.title_var = StringVar()
        self.author_var = StringVar()
        self.genre_var = StringVar()
        self.year_var = StringVar()
        self.notes_var = StringVar()
        self.rating_var = StringVar()
        self.shelf_var = StringVar()

        self.create_widgets()

    def create_widgets(self) -> None:
        tk.Label(self.root, text="Title").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.title_var).grid(row=0, column=1)

        tk.Label(self.root, text="Author").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.author_var).grid(row=1, column=1)

        tk.Label(self.root, text="Genre").grid(row=2, column=0)
        tk.Entry(self.root, textvariable=self.genre_var).grid(row=2, column=1)

        tk.Label(self.root, text="Year").grid(row=3, column=0)
        tk.Entry(self.root, textvariable=self.year_var).grid(row=3, column=1)

        tk.Label(self.root, text="Notes").grid(row=4, column=0)
        tk.Entry(self.root, textvariable=self.notes_var).grid(row=4, column=1)

        tk.Label(self.root, text="Rating").grid(row=5, column=0)
        tk.Entry(self.root, textvariable=self.rating_var).grid(row=5, column=1)

        tk.Label(self.root, text="Shelf").grid(row=6, column=0)
        tk.Entry(self.root, textvariable=self.shelf_var).grid(row=6, column=1)

        Button(self.root, text="Add Book", command=self.add_book).grid(row=7, column=0, columnspan=2)

        self.listbox = Listbox(self.root)
        self.listbox.grid(row=8, column=0, columnspan=2)

        self.load_books()

    def load_books(self) -> None:
        self.listbox.delete(0, tk.END)
        for book in self.book_manager.books:
            self.listbox.insert(tk.END, book.title)

    def add_book(self) -> None:
        try:
            title = self.title_var.get()
            author = self.author_var.get()
            genre = self.genre_var.get()
            year = int(self.year_var.get())
            notes = self.notes_var.get()
            rating = float(self.rating_var.get())
            shelf = self.shelf_var.get()

            self.book_manager.add_book(title, author, genre, year, notes, rating, shelf)
            self.load_books()
            messagebox.showinfo("Success", "Book added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid data.")