import os
import tempfile

class BookManager:
    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(file_path):
            open(file_path, 'w').close()

    def add_book(self, title, author, isbn):
        books = self.list_books()
        if any(book[2] == isbn for book in books):
            raise ValueError("Book with this ISBN already exists")
        
        with open(self.file_path, 'a') as f:
            f.write(f"{title}|{author}|{isbn}\n")

    def delete_book(self, isbn):
        books = self.list_books()
        updated_books = [book for book in books if book[2] != isbn]
        
        if len(updated_books) == len(books):
            raise ValueError("Book not found")
        
        temp_path = tempfile.mktemp()
        with open(temp_path, 'w') as f:
            for book in updated_books:
                f.write(f"{book[0]}|{book[1]}|{book[2]}\n")
        
        os.replace(temp_path, self.file_path)

    def list_books(self):
        books = []
        with open(self.file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    title, author, isbn = line.split('|')
                    books.append((title, author, isbn))
        return books

    def search_books(self, query):
        query = query.lower()
        books = self.list_books()
        return [book for book in books 
                if query in book[0].lower() 
                or query in book[1].lower() 
                or query in book[2].lower()]