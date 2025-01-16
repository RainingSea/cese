class Book:
    def __init__(self, title='', author='', content=''):
        self.title = title
        self.author = author
        self.content = content

    def save(self):
        with open('books.txt', 'a') as f:
            f.write(f"{self.title}|{self.author}|{self.content}\n")

    def load_books(self):
        books = []
        try:
            with open('books.txt', 'r') as f:
                for line in f:
                    title, author, content = line.strip().split('|')
                    books.append(Book(title, author, content))
        except FileNotFoundError:
            pass
        return books

    def create_book(self, title, author, content):
        self.title = title
        self.author = author
        self.content = content
        self.save()

    def view_book_details(self, title):
        for book in self.load_books():
            if book.title == title:
                return {'title': book.title, 'author': book.author, 'content': book.content}
        return None