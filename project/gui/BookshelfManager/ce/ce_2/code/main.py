import tkinter as tk
from book_manager import BookManager

class Main:
    def __init__(self):
        self.book_manager = BookManager()
        self.root = tk.Tk()
        self.root.title("Bookshelf Manager")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Title").grid(row=0, column=0)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Author").grid(row=1, column=0)
        self.author_entry = tk.Entry(self.root)
        self.author_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Genre").grid(row=2, column=0)
        self.genre_entry = tk.Entry(self.root)
        self.genre_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Year").grid(row=3, column=0)
        self.year_entry = tk.Entry(self.root)
        self.year_entry.grid(row=3, column=1)

        tk.Button(self.root, text="Add Book", command=self.add_book).grid(row=4, columnspan=2)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        year = int(self.year_entry.get())
        self.book_manager.add_book(title, author, genre, year)
        self.clear_entries()

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()