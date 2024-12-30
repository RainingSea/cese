class BookManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.load_books()

    def load_books(self):
        self.books = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    title, author = line.strip().split('|')
                    self.books.append({'title': title, 'author': author})
        except FileNotFoundError:
            open(self.filename, 'w').close()  # Create the file if it doesn't exist

    def add_book(self, title: str, author: str) -> bool:
        self.books.append({'title': title, 'author': author})
        with open(self.filename, 'a') as file:
            file.write(f"{title}|{author}\n")
        return True

    def delete_book(self, title: str) -> bool:
        for book in self.books:
            if book['title'] == title:
                self.books.remove(book)
                self.save_books()
                return True
        return False

    def save_books(self):
        with open(self.filename, 'w') as file:
            for book in self.books:
                file.write(f"{book['title']}|{book['author']}\n")

    def list_books(self) -> list:
        return self.books

    def search_books(self, query: str) -> list:
        results = []
        for book in self.books:
            if query.lower() in book['title'].lower() or query.lower() in book['author'].lower():
                results.append(book)
        return results