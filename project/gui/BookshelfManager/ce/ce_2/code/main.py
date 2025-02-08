import tkinter as tk
from tkinter import messagebox
from book_manager import BookManager

class Main:
    def __init__(self, root):
        self.book_manager = BookManager()
        self.root = root
        self.root.title("Bookshelf Manager")

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Title:")
        self.title_label.grid(row=0, column=0)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1)

        self.author_label = tk.Label(self.root, text="Author:")
        self.author_label.grid(row=1, column=0)
        self.author_entry = tk.Entry(self.root)
        self.author_entry.grid(row=1, column=1)

        self.genre_label = tk.Label(self.root, text="Genre:")
        self.genre_label.grid(row=2, column=0)
        self.genre_entry = tk.Entry(self.root)
        self.genre_entry.grid(row=2, column=1)

        self.year_label = tk.Label(self.root, text="Publication Year:")
        self.year_label.grid(row=3, column=0)
        self.year_entry = tk.Entry(self.root)
        self.year_entry.grid(row=3, column=1)

        self.notes_label = tk.Label(self.root, text="Notes:")
        self.notes_label.grid(row=4, column=0)
        self.notes_entry = tk.Entry(self.root)
        self.notes_entry.grid(row=4, column=1)

        self.rating_label = tk.Label(self.root, text="Rating:")
        self.rating_label.grid(row=5, column=0)
        self.rating_entry = tk.Entry(self.root)
        self.rating_entry.grid(row=5, column=1)

        self.add_button = tk.Button(self.root, text="Add Book", command=self.add_book)
        self.add_button.grid(row=6, columnspan=2)

    def add_book(self):
        try:
            title = self.title_entry.get()
            author = self.author_entry.get()
            genre = self.genre_entry.get()
            year = int(self.year_entry.get())
            notes = self.notes_entry.get()
            rating = float(self.rating_entry.get())

            self.book_manager.add_book(title, author, genre, year, notes, rating)
            messagebox.showinfo("Success", "Book added successfully.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid data.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()