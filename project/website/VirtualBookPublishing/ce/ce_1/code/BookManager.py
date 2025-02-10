class Book:
    def __init__(self, title: str, author: str, content: str):
        self.title = title
        self.author = author
        self.content = content

    def save(self):
        with open('books.txt', 'a') as f:
            f.write(f'{self.title}|{self.author}|{self.content}\n')

class BookManager:
    def __init__(self, books_file: str):
        self.books_file = books_file

    def add_book(self, title: str, author: str, content: str):
        book = Book(title, author, content)
        book.save()

    def get_books(self) -> list:
        books = []
        with open(self.books_file, 'r') as f:
            for line in f:
                title, author, _ = line.strip().split('|')
                books.append({'title': title, 'author': author})
        return books

    def get_book_details(self, title: str) -> Book:
        with open(self.books_file, 'r') as f:
            for line in f:
                book_title, author, content = line.strip().split('|')
                if book_title == title:
                    return Book(book_title, author, content)
        return None