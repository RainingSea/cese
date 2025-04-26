class BookManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.load_books()

    def load_books(self):
        self.books = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    title, author, content = line.strip().split('|')
                    self.books.append({'title': title, 'author': author, 'content': content})
        except FileNotFoundError:
            pass

    def create_book(self, title: str, author: str, content: str) -> bool:
        self.books.append({'title': title, 'author': author, 'content': content})
        with open(self.filename, 'a') as file:
            file.write(f"{title}|{author}|{content}\n")
        return True

    def get_books(self) -> list:
        return [{'title': book['title'], 'author': book['author']} for book in self.books]

    def get_book_details(self, title: str) -> str:
        for book in self.books:
            if book['title'] == title:
                return f"Title: {book['title']}\nAuthor: {book['author']}\nContent: {book['content']}"
        return "Book not found."