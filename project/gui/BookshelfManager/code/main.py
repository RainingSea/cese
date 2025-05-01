import tkinter as tk
from file_handler import FileHandler
from book_manager import BookManager
from ui import UI

def main() -> None:
    file_handler = FileHandler('books.txt', 'shelves.txt', 'reports.txt')
    book_manager = BookManager(file_handler)

    root = tk.Tk()
    app = UI(root, book_manager)
    root.mainloop()

if __name__ == "__main__":
    main()