class BookManager:
    def __init__(self):
        self.books = self.load_books()

    def load_books(self):
        books = []
        try:
            with open('books.txt', 'r') as file:
                for line in file:
                    title, author, year = line.strip().split('|')
                    books.append((title, author, int(year)))
        except FileNotFoundError:
            pass
        return books

    def add_book(self, title: str, author: str, year: int) -> bool:
        if any(book[0] == title for book in self.books):
            return False
        self.books.append((title, author, year))
        with open('books.txt', 'a') as file:
            file.write(f'{title}|{author}|{year}\n')
        return True

    def delete_book(self, title: str) -> None:
        self.books = [book for book in self.books if book[0] != title]
        self.save_books()

    def save_books(self):
        with open('books.txt', 'w') as file:
            for book in self.books:
                file.write(f'{book[0]}|{book[1]}|{book[2]}\n')

    def get_books(self) -> list:
        return self.books

    def search_books(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book[0].lower() or query.lower() in book[1].lower()]