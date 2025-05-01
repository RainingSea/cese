import tkinter as tk
from tkinter import messagebox
import os
import csv

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Bookshelf Manager")
        self.book_manager = BookManager()
        self.create_widgets()

    def create_widgets(self):
        # Input fields
        tk.Label(self.root, text="Title").grid(row=0, column=0)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Author").grid(row=1, column=0)
        self.author_entry = tk.Entry(self.root)
        self.author_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Genre").grid(row=2, column=0)
        self.genre_entry = tk.Entry(self.root)
        self.genre_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Publication Year").grid(row=3, column=0)
        self.year_entry = tk.Entry(self.root)
        self.year_entry.grid(row=3, column=1)

        # Buttons
        tk.Button(self.root, text="Add Book", command=self.add_book).grid(row=4, column=0, columnspan=2)
        tk.Button(self.root, text="Generate Report", command=self.generate_report).grid(row=5, column=0, columnspan=2)

        # Listbox for displaying books
        self.books_listbox = tk.Listbox(self.root)
        self.books_listbox.grid(row=6, column=0, columnspan=2)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        year = self.year_entry.get()

        if title and author and genre and year.isdigit():
            self.book_manager.add_book(title, author, genre, int(year))
            self.update_books_listbox()
            self.clear_entries()
        else:
            messagebox.showerror("Input Error", "Please fill all fields correctly.")

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)

    def update_books_listbox(self):
        self.books_listbox.delete(0, tk.END)
        for book in self.book_manager.books:
            self.books_listbox.insert(tk.END, f"{book.title} by {book.author}")

    def generate_report(self):
        report = self.book_manager.generate_report()
        messagebox.showinfo("Report", report)

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()