class Book:
    def __init__(self, username: str, title: str, author: str, content: str):
        self.username = username
        self.title = title
        self.author = author
        self.content = content

    def save(self):
        with open('books.txt', 'a') as file:
            file.write(f"{self.username}|{self.title}|{self.author}|{self.content}\n")

class BookManager:
    def create_book(self, username: str, title: str, author: str, content: str):
        book = Book(username, title, author, content)
        book.save()

    def load_books(self, username: str) -> list:
        books = []
        try:
            with open('books.txt', 'r') as file:
                for line in file:
                    user, title, author, content = line.strip().split('|')
                    if user == username:
                        books.append(Book(user, title, author, content))
        except FileNotFoundError:
            pass
        return books

    def get_book_details(self, title: str) -> Book:
        books = self.load_books('')
        for book in books:
            if book.title == title:
                return book
        return None