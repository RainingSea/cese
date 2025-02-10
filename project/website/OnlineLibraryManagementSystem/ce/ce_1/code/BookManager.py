from Book import Book

class BookManager:
    def add_book(self, title: str, author: str, isbn: str) -> None:
        book = Book(title, author, isbn)
        book.save()

    def get_books(self) -> list:
        return Book.load_books()

    def delete_book(self, isbn: str) -> None:
        books = self.get_books()
        with open('books.txt', 'w') as file:
            for book in books:
                if book.isbn != isbn:
                    file.write(f"{book.title}|{book.author}|{book.isbn}\n")