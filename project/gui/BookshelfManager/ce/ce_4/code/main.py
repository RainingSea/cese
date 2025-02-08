import tkinter as tk
from tkinter import messagebox
from books import BookManager
from data_management import load_books_from_file, save_books_to_file

class Main:
    def __init__(self):
        self.book_manager = BookManager()
        self.book_manager.load_books()
        self.root = tk.Tk()
        self.root.title("Book Collection Manager")
        self.create_widgets()

    def create_widgets(self):
        self.add_button = tk.Button(self.root, text="Add Book", command=self.add_book)
        self.add_button.pack()

        self.view_button = tk.Button(self.root, text="View Reports", command=self.view_reports)
        self.view_button.pack()

        self.search_button = tk.Button(self.root, text="Search Books", command=self.search_books)
        self.search_button.pack()

        self.filter_button = tk.Button(self.root, text="Filter Books", command=self.filter_books)
        self.filter_button.pack()

        self.book_list = tk.Text(self.root)
        self.book_list.pack()

    def add_book(self):
        # Example input for demonstration purposes
        self.book_manager.add_book("The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 1925, "Classic American novel", 4.5)
        self.book_manager.save_books()
        messagebox.showinfo("Success", "Book added successfully!")

    def view_reports(self):
        report = self.book_manager.generate_report()
        self.book_list.delete(1.0, tk.END)
        self.book_list.insert(tk.END, report)

    def search_books(self):
        # Example search for demonstration purposes
        results = self.book_manager.search_books("Gatsby")
        self.book_list.delete(1.0, tk.END)
        for book in results:
            self.book_list.insert(tk.END, f"{book.title} by {book.author}\n")

    def filter_books(self):
        # Example filter for demonstration purposes
        results = self.book_manager.filter_books({'genre': 'Fiction'})
        self.book_list.delete(1.0, tk.END)
        for book in results:
            self.book_list.insert(tk.END, f"{book.title} by {book.author}\n")

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()