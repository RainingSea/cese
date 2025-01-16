class BookManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.books = self.load_books()

    def load_books(self) -> list:
        books = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    title, author, content = line.strip().split('|')
                    books.append({'title': title, 'author': author, 'content': content})
        except FileNotFoundError:
            pass
        return books

    def create_book(self, title: str, author: str, content: str) -> bool:
        if any(book['title'] == title for book in self.books):
            return False
        self.books.append({'title': title, 'author': author, 'content': content})
        with open(self.filename, 'a') as file:
            file.write(f"{title}|{author}|{content}\n")
        return True

    def get_books(self) -> list:
        return self.books

    def get_book_details(self, title: str) -> dict:
        for book in self.books:
            if book['title'] == title:
                return book
        return {}