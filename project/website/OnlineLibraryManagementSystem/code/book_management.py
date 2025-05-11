class BookManager:
    def __init__(self):
        self.books = []

    def add_book(self, title: str, author: str) -> bool:
        if any(book[0] == title for book in self.books):
            return False
        self.books.append((title, author))
        self.save_books()
        return True

    def delete_book(self, title: str) -> bool:
        for book in self.books:
            if book[0] == title:
                self.books.remove(book)
                self.save_books()
                return True
        return False

    def view_books(self) -> list:
        return self.books

    def search_books(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book[0].lower() or query.lower() in book[1].lower()]

    def load_books(self) -> None:
        try:
            with open('books.txt', 'r') as file:
                for line in file:
                    title, author = line.strip().split('|')
                    self.books.append((title, author))
        except FileNotFoundError:
            pass

    def save_books(self) -> None:
        with open('books.txt', 'w') as file:
            for title, author in self.books:
                file.write(f"{title}|{author}\n")