import tkinter as tk
from tkinter import messagebox
from book_manager import BookManager

class Main:
    def __init__(self):
        self.book_manager = BookManager()
        self.root = tk.Tk()
        self.root.title("Bookshelf Manager")
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()
        self.author_entry = tk.Entry(self.root)
        self.author_entry.pack()
        self.genre_entry = tk.Entry(self.root)
        self.genre_entry.pack()
        self.year_entry = tk.Entry(self.root)
        self.year_entry.pack()
        self.shelf_entry = tk.Entry(self.root)
        self.shelf_entry.pack()
        self.notes_entry = tk.Entry(self.root)
        self.notes_entry.pack()
        self.rating_entry = tk.Entry(self.root)
        self.rating_entry.pack()

        add_button = tk.Button(self.root, text="Add Book", command=self.add_book)
        add_button.pack()

        report_button = tk.Button(self.root, text="Generate Report", command=self.generate_report)
        report_button.pack()

        self.books_listbox = tk.Listbox(self.root)
        self.books_listbox.pack()

        self.update_books_listbox()

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        year = int(self.year_entry.get())
        shelf = self.shelf_entry.get()
        notes = self.notes_entry.get()
        rating = float(self.rating_entry.get())
        
        self.book_manager.add_book(title, author, genre, year, shelf, notes, rating)
        self.update_books_listbox()
        messagebox.showinfo("Success", "Book added successfully!")

    def generate_report(self):
        report = self.book_manager.generate_report()
        report_message = f"Total Books: {report['total_books']}\nAverage Rating: {report['average_rating']}\nShelves: {', '.join(report['shelves'])}"
        messagebox.showinfo("Report", report_message)

    def update_books_listbox(self):
        self.books_listbox.delete(0, tk.END)
        for book in self.book_manager.books:
            self.books_listbox.insert(tk.END, f"{book.title} by {book.author}")