import tkinter as tk
from tkinter import messagebox
from book_manager import BookManager
from note_manager import NoteManager
from category_manager import CategoryManager
from search_engine import SearchEngine

class Main:
    def __init__(self):
        self.book_manager = BookManager()
        self.note_manager = NoteManager()
        self.category_manager = CategoryManager()
        self.search_engine = SearchEngine()
        self.setup_ui()

    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("BookNote Application")

        self.book_title_entry = tk.Entry(self.root)
        self.book_title_entry.pack()
        self.book_author_entry = tk.Entry(self.root)
        self.book_author_entry.pack()
        self.book_pub_date_entry = tk.Entry(self.root)
        self.book_pub_date_entry.pack()

        self.add_book_button = tk.Button(self.root, text="Add Book", command=self.add_book)
        self.add_book_button.pack()

        self.note_chapter_entry = tk.Entry(self.root)
        self.note_chapter_entry.pack()
        self.note_text_entry = tk.Text(self.root, height=5, width=40)
        self.note_text_entry.pack()
        self.note_category_entry = tk.Entry(self.root)
        self.note_category_entry.pack()

        self.add_note_button = tk.Button(self.root, text="Add Note", command=self.add_note)
        self.add_note_button.pack()

        self.category_entry = tk.Entry(self.root)
        self.category_entry.pack()

        self.add_category_button = tk.Button(self.root, text="Add Category", command=self.add_category)
        self.add_category_button.pack()

        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack()
        self.search_button = tk.Button(self.root, text="Search Books", command=self.search_books)
        self.search_button.pack()

        self.root.mainloop()

    def add_book(self):
        title = self.book_title_entry.get()
        author = self.book_author_entry.get()
        pub_date = self.book_pub_date_entry.get()
        if title and author and pub_date:
            self.book_manager.add_book(title, author, pub_date)
            messagebox.showinfo("Success", "Book added successfully!")
        else:
            messagebox.showwarning("Warning", "Please fill all fields.")

    def add_note(self):
        chapter = self.note_chapter_entry.get()
        text = self.note_text_entry.get("1.0", tk.END).strip()
        category = self.note_category_entry.get()
        book_title = self.book_title_entry.get()
        if book_title and chapter and text and category:
            self.note_manager.add_note(book_title, chapter, text, category)
            messagebox.showinfo("Success", "Note added successfully!")
        else:
            messagebox.showwarning("Warning", "Please fill all fields.")

    def add_category(self):
        name = self.category_entry.get()
        if name:
            self.category_manager.add_category(name)
            messagebox.showinfo("Success", "Category added successfully!")
        else:
            messagebox.showwarning("Warning", "Please fill the category field.")

    def search_books(self):
        query = self.search_entry.get()
        results = self.search_engine.search_books(query, self.book_manager)
        if results:
            messagebox.showinfo("Search Results", "\n".join([book.title for book in results]))
        else:
            messagebox.showinfo("Search Results", "No books found.")

def main():
    app = Main()

if __name__ == "__main__":
    main()