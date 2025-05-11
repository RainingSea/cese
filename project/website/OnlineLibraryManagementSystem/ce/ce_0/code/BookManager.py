class BookManager:
    def __init__(self):
        self.books = []
        self.load_books()

    def add_book(self, title: str, author: str) -> bool:
        if any(book[0] == title for book in self.books):
            return False
        self.books.append((title, author))
        self.save_books()
        return True

    def delete_book(self, title: str) -> bool:
        self.books = [book for book in self.books if book[0] != title]
        self.save_books()
        return True

    def view_books(self) -> list:
        return self.books

    def load_books(self) -> None:
        try:
            with open('books.txt', 'r') as file:
                self.books = [line.strip().split('|') for line in file.readlines()]
        except FileNotFoundError:
            self.books = []

    def save_books(self) -> None:
        with open('books.txt', 'w') as file:
            for book in self.books:
                file.write('|'.join(book) + '\n')

    def search_books(self, query: str) -> list:
        results = [book for book in self.books if query.lower() in book[0].lower()]
        return results