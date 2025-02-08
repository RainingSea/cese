import tkinter as tk
from tkinter import messagebox, simpledialog
from bookshelf_manager import BookshelfManager
from book import Book

class MainApp:
    def __init__(self, root):
        self.manager = BookshelfManager()
        self.root = root
        self.root.title("Bookshelf Manager")

        self.create_widgets()
        self.manager.load_books('books.txt')

    def create_widgets(self):
        self.title_entry = tk.Entry(self.root)
        self.title_entry.pack()
        self.author_entry = tk.Entry(self.root)
        self.author_entry.pack()
        self.genre_entry = tk.Entry(self.root)
        self.genre_entry.pack()
        self.year_entry = tk.Entry(self.root)
        self.year_entry.pack()

        self.add_button = tk.Button(self.root, text="Add Book", command=self.add_book_ui)
        self.add_button.pack()

        self.listbox = tk.Listbox(self.root)
        self.listbox.pack()

        self.report_button = tk.Button(self.root, text="Generate Report", command=self.report_ui)
        self.report_button.pack()

    def add_book_ui(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        publication_year = self.year_entry.get()

        if title and author and genre and publication_year.isdigit():
            book = Book(title, author, genre, int(publication_year))
            self.manager.add_book(book)
            self.manager.save_books('books.txt')
            self.listbox.insert(tk.END, book.to_string())
            self.clear_entries()
        else:
            messagebox.showerror("Input Error", "Please fill all fields correctly.")

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)

    def report_ui(self):
        report = self.manager.generate_report()
        messagebox.showinfo("Report", f"Total Books: {report['total_books']}\nAverage Rating: {report['average_rating']:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()