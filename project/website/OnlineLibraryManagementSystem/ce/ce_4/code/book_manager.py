class BookManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.load_books()

    def load_books(self):
        self.books = {}
        with open(self.filepath, 'r') as file:
            for line in file:
                title, author = line.strip().split('|')
                self.books[title] = author

    def add_book(self, title: str, author: str) -> bool:
        if title in self.books:
            return False
        self.books[title] = author
        with open(self.filepath, 'a') as file:
            file.write(f"{title}|{author}\n")
        return True

    def delete_book(self, title: str) -> bool:
        if title not in self.books:
            return False
        del self.books[title]
        self.save_books()
        return True

    def save_books(self):
        with open(self.filepath, 'w') as file:
            for title, author in self.books.items():
                file.write(f"{title}|{author}\n")

    def list_books(self) -> list:
        return list(self.books.items())