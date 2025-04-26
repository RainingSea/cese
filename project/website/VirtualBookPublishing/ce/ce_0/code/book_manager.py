class BookManager:
    def __init__(self, books_file: str):
        self.books_file = books_file

    def create_book(self, title: str, author: str, content: str) -> bool:
        with open(self.books_file, 'a') as file:
            file.write(f"{title}|{author}|{content}\n")
        return True

    def get_books(self) -> list:
        books = []
        with open(self.books_file, 'r') as file:
            for line in file:
                title, author, _ = line.strip().split('|')
                books.append({'title': title, 'author': author})
        return books

    def get_book_details(self, title: str) -> str:
        with open(self.books_file, 'r') as file:
            for line in file:
                if line.startswith(title):
                    return line.strip()
        return "Book not found."