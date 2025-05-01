import tkinter as tk
from tkinter import messagebox, simpledialog
from book_manager import BookManager

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Bookshelf Manager")
        self.book_manager = BookManager()
        self.book_manager.load_data()
        self.create_widgets()

    def create_widgets(self):
        # Input Form
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

        tk.Label(self.root, text="Notes").grid(row=4, column=0)
        self.notes_entry = tk.Entry(self.root)
        self.notes_entry.grid(row=4, column=1)

        tk.Label(self.root, text="Rating").grid(row=5, column=0)
        self.rating_entry = tk.Entry(self.root)
        self.rating_entry.grid(row=5, column=1)

        tk.Label(self.root, text="Shelf").grid(row=6, column=0)
        self.shelf_entry = tk.Entry(self.root)
        self.shelf_entry.grid(row=6, column=1)

        tk.Button(self.root, text="Add Book", command=self.add_book).grid(row=7, column=0, columnspan=2)
        tk.Button(self.root, text="Generate Report", command=self.generate_report).grid(row=8, column=0, columnspan=2)

        # Search and Filter
        tk.Label(self.root, text="Search").grid(row=9, column=0)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=9, column=1)
        tk.Button(self.root, text="Search", command=self.search_books).grid(row=10, column=0, columnspan=2)

        tk.Label(self.root, text="Filter").grid(row=11, column=0)
        self.filter_entry = tk.Entry(self.root)
        self.filter_entry.grid(row=11, column=1)
        tk.Button(self.root, text="Filter", command=self.filter_books).grid(row=12, column=0, columnspan=2)

        # Display Area
        self.display_area = tk.Listbox(self.root, width=50)
        self.display_area.grid(row=13, column=0, columnspan=2)

        # Status Bar
        self.status_bar = tk.Label(self.root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=14, column=0, columnspan=2, sticky=tk.W + tk.E)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        year = self.year_entry.get()
        notes = self.notes_entry.get()
        rating = self.rating_entry.get()
        shelf = self.shelf_entry.get()

        try:
            year = int(year)
            rating = float(rating)
            self.book_manager.add_book(title, author, genre, year, notes, rating, shelf)
            self.status_bar.config(text="Book added successfully.")
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid data for year and rating.")

    def generate_report(self):
        report = self.book_manager.generate_report()
        messagebox.showinfo("Book Report", report)

    def search_books(self):
        query = self.search_entry.get()
        results = self.book_manager.search_books(query)
        self.display_results(results)

    def filter_books(self):
        criteria = self.filter_entry.get()
        results = self.book_manager.filter_books(criteria)
        self.display_results(results)

    def display_results(self, results):
        self.display_area.delete(0, tk.END)
        for book in results:
            self.display_area.insert(tk.END, book)

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)
        self.shelf_entry.delete(0, tk.END)

    @staticmethod
    def main():
        root = tk.Tk()
        app = Main(root)
        root.mainloop()

if __name__ == "__main__":
    Main.main()