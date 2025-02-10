class BookManager:
    def __init__(self, books_file: str, reading_list_file: str):
        self.books_file = books_file
        self.reading_list_file = reading_list_file
        self.books = self.load_books()

    def search_books(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book['title'].lower()]

    def load_books(self) -> list:
        books = []
        try:
            with open(self.books_file, 'r') as f:
                for line in f:
                    title, author, description = line.strip().split('|')
                    books.append({'title': title, 'author': author, 'description': description})
        except FileNotFoundError:
            pass
        return books

    def add_to_reading_list(self, username: str, book: dict) -> bool:
        with open(self.reading_list_file, 'a') as f:
            f.write(f"{username}|{book['title']}\n")
        return True

    def get_reading_list(self, username: str) -> list:
        reading_list = []
        try:
            with open(self.reading_list_file, 'r') as f:
                for line in f:
                    user, book_title = line.strip().split('|')
                    if user == username:
                        reading_list.append(book_title)
        except FileNotFoundError:
            pass
        return reading_list