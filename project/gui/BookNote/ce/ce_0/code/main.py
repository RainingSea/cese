import tkinter as tk
from tkinter import messagebox
from books.BookManager import BookManager

class BookNoteApp:
    def __init__(self) -> None:
        self.book_manager = BookManager()
        self.book_manager.load_books()
        self.root = tk.Tk()
        self.root.title("BookNote Application")
        self.create_widgets()

    def create_widgets(self) -> None:
        self.title_entry = tk.Entry(self.root, width=50)
        self.title_entry.pack(pady=10)
        self.author_entry = tk.Entry(self.root, width=50)
        self.author_entry.pack(pady=10)
        self.genre_entry = tk.Entry(self.root, width=50)
        self.genre_entry.pack(pady=10)
        self.pub_date_entry = tk.Entry(self.root, width=50)
        self.pub_date_entry.pack(pady=10)

        self.add_book_button = tk.Button(self.root, text="Add Book", command=self.add_book)
        self.add_book_button.pack(pady=20)

        self.chapter_entry = tk.Entry(self.root, width=50)
        self.chapter_entry.pack(pady=10)
        self.note_entry = tk.Entry(self.root, width=50)
        self.note_entry.pack(pady=10)

        self.add_note_button = tk.Button(self.root, text="Add Note", command=self.add_note)
        self.add_note_button.pack(pady=20)

        self.search_entry = tk.Entry(self.root, width=50)
        self.search_entry.pack(pady=10)
        self.search_button = tk.Button(self.root, text="Search", command=self.search)
        self.search_button.pack(pady=20)

    def add_book(self) -> None:
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        pub_date = self.pub_date_entry.get()
        self.book_manager.add_book(title, author, genre, pub_date)
        messagebox.showinfo("Success", f"Book '{title}' added successfully!")

    def add_note(self) -> None:
        title = self.title_entry.get()
        chapter = int(self.chapter_entry.get())
        note = self.note_entry.get()
        self.book_manager.add_note_to_chapter(title, chapter, note)
        messagebox.showinfo("Success", f"Note added to '{title}', Chapter {chapter}!")

    def search(self) -> None:
        query = self.search_entry.get()
        results = self.book_manager.search_books(query)
        if results:
            messagebox.showinfo("Search Results", "\n".join(results))
        else:
            messagebox.showinfo("Search Results", "No books found.")

    def run(self) -> None:
        self.root.mainloop()

if __name__ == "__main__":
    app = BookNoteApp()
    app.run()