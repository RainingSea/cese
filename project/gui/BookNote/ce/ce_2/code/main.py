import tkinter as tk
from tkinter import messagebox, simpledialog
from data_manager import DataManager

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("BookNote Application")
        self.data_manager = DataManager()

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.master, text="Book Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.master)
        self.title_entry.pack()

        self.author_label = tk.Label(self.master, text="Author:")
        self.author_label.pack()
        self.author_entry = tk.Entry(self.master)
        self.author_entry.pack()

        self.pub_date_label = tk.Label(self.master, text="Publication Date:")
        self.pub_date_label.pack()
        self.pub_date_entry = tk.Entry(self.master)
        self.pub_date_entry.pack()

        self.add_book_button = tk.Button(self.master, text="Add Book", command=self.add_book)
        self.add_book_button.pack()

        self.note_label = tk.Label(self.master, text="Chapter Note:")
        self.note_label.pack()
        self.note_entry = tk.Entry(self.master)
        self.note_entry.pack()

        self.add_note_button = tk.Button(self.master, text="Add Note", command=self.add_note)
        self.add_note_button.pack()

        self.search_label = tk.Label(self.master, text="Search:")
        self.search_label.pack()
        self.search_entry = tk.Entry(self.master)
        self.search_entry.pack()

        self.search_books_button = tk.Button(self.master, text="Search Books", command=self.search_books)
        self.search_books_button.pack()

        self.search_notes_button = tk.Button(self.master, text="Search Notes", command=self.search_notes)
        self.search_notes_button.pack()

    def main(self):
        self.master.mainloop()

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        pub_date = self.pub_date_entry.get()
        self.data_manager.save_book(title, author, pub_date)
        messagebox.showinfo("Success", "Book added successfully!")

    def add_note(self):
        book_id = simpledialog.askinteger("Input", "Enter Book ID:")
        chapter = simpledialog.askstring("Input", "Enter Chapter:")
        note = self.note_entry.get()
        self.data_manager.save_note(book_id, chapter, note)
        messagebox.showinfo("Success", "Note added successfully!")

    def search_books(self):
        query = self.search_entry.get()
        results = self.data_manager.load_books()
        matching_books = [book for book in results if query.lower() in book.lower()]
        messagebox.showinfo("Search Results", "\n".join(matching_books))

    def search_notes(self):
        query = self.search_entry.get()
        results = self.data_manager.load_notes()
        matching_notes = [note for note in results if query.lower() in note.lower()]
        messagebox.showinfo("Search Results", "\n".join(matching_notes))


if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.main()