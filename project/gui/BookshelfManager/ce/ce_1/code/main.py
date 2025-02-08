import tkinter as tk
from tkinter import messagebox
from BookManager import BookManager

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Bookshelf Manager")
        self.book_manager = BookManager()
        
        self.create_widgets()

    def create_widgets(self):
        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()

        self.author_entry = tk.Entry(self.root)
        self.author_entry.pack()

        self.genre_entry = tk.Entry(self.root)
        self.genre_entry.pack()

        self.year_entry = tk.Entry(self.root)
        self.year_entry.pack()

        self.notes_entry = tk.Entry(self.root)
        self.notes_entry.pack()

        self.rating_entry = tk.Entry(self.root)
        self.rating_entry.pack()

        self.add_button = tk.Button(self.root, text="Add Book", command=self.add_book)
        self.add_button.pack()

        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack()

        self.search_button = tk.Button(self.root, text="Search Books", command=self.search_books)
        self.search_button.pack()

        self.listbox = tk.Listbox(self.root)
        self.listbox.pack()

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        year = int(self.year_entry.get())
        notes = self.notes_entry.get()
        rating = float(self.rating_entry.get())

        self.book_manager.add_book(title, author, genre, year, notes, rating)
        messagebox.showinfo("Success", "Book added successfully!")

    def search_books(self):
        query = self.search_entry.get()
        results = self.book_manager.search_books(query)
        self.listbox.delete(0, tk.END)
        for book in results:
            self.listbox.insert(tk.END, f"{book.title} by {book.author}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()