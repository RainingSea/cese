class Book:
    def __init__(self):
        self.books_file = 'books.txt'

    def load_books(self) -> list:
        books = []
        try:
            with open(self.books_file, 'r') as file:
                for line in file:
                    title, author, summary = line.strip().split('|')
                    books.append({'title': title, 'author': author, 'summary': summary})
        except FileNotFoundError:
            pass
        return books

    def save_books(self, books: list):
        with open(self.books_file, 'w') as file:
            for book in books:
                file.write(f"{book['title']}|{book['author']}|{book['summary']}\n")