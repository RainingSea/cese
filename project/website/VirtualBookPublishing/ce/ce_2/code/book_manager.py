class BookManager:
    def __init__(self, books_file: str):
        self.books_file = books_file
        self.load_books()

    def load_books(self):
        self.books = []
        with open(self.books_file, 'r') as file:
            for line in file:
                username, title, author, content = line.strip().split(':')
                self.books.append({'username': username, 'title': title, 'author': author, 'content': content})

    def create_book(self, username: str, title: str, author: str, content: str) -> None:
        with open(self.books_file, 'a') as file:
            file.write(f"{username}:{title}:{author}:{content}\n")
        self.books.append({'username': username, 'title': title, 'author': author, 'content': content})

    def get_books(self, username: str) -> list:
        return [book for book in self.books if book['username'] == username]

    def get_book_details(self, title: str) -> str:
        for book in self.books:
            if book['title'] == title:
                return f"Title: {book['title']}\nAuthor: {book['author']}\nContent: {book['content']}"
        return "Book not found."