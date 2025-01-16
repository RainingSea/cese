class BookManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.load_books()

    def load_books(self):
        self.books = []
        with open(self.file_path, 'r') as file:
            for line in file:
                title, author, content = line.strip().split('|')
                self.books.append({'title': title, 'author': author, 'content': content})

    def create_book(self, title: str, author: str, content: str) -> bool:
        self.books.append({'title': title, 'author': author, 'content': content})
        with open(self.file_path, 'a') as file:
            file.write(f"{title}|{author}|{content}\n")
        return True

    def get_user_books(self, username: str) -> list:
        # For simplicity, returning all books as we don't have user-book mapping
        return self.books

    def get_book_details(self, book_id: int) -> dict:
        if 0 <= book_id < len(self.books):
            return self.books[book_id]
        return {}