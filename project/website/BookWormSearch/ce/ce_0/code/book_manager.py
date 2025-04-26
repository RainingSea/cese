class BookManager:
    def __init__(self):
        self.books = []

    def search_books(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book['title'].lower()]

    def load_books(self) -> None:
        try:
            with open('books.txt', 'r') as f:
                for line in f:
                    title, author, summary = line.strip().split('|')
                    self.books.append({'title': title, 'author': author, 'summary': summary})
        except FileNotFoundError:
            pass

    def add_to_reading_list(self, username: str, book_id: str) -> None:
        with open(f"{username}_reading_list.txt", 'a') as f:
            f.write(f"{book_id}\n")