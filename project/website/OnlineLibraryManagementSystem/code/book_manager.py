import os

class BookManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.load_books()

    def load_books(self):
        self.books = []
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                for line in file:
                    title, author = line.strip().split('|')
                    self.books.append({'title': title, 'author': author})

    def add_book(self, title: str, author: str) -> bool:
        if any(book['title'] == title for book in self.books):
            return False  # Book already exists
        self.books.append({'title': title, 'author': author})
        self.save_books()
        return True

    def delete_book(self, title: str) -> bool:
        if any(book['title'] == title for book in self.books):
            self.books = [book for book in self.books if book['title'] != title]
            self.save_books()
            return True
        return False  # Book not found

    def list_books(self) -> list:
        return self.books

    def save_books(self):
        with open(self.file_path, 'w') as file:
            for book in self.books:
                file.write(f"{book['title']}|{book['author']}\n")

    def search_book(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book['title'].lower()]