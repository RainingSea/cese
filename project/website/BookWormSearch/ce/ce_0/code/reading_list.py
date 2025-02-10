class ReadingList:
    def __init__(self, username: str):
        self.username = username
        self.reading_list_file = f"{username}_reading_list.txt"

    def add_book(self, book: dict):
        books = self.load_reading_list()
        books.append(book)
        self.save_reading_list(books)

    def remove_book(self, book: dict):
        books = self.load_reading_list()
        books.remove(book)
        self.save_reading_list(books)

    def load_reading_list(self) -> list:
        books = []
        try:
            with open(self.reading_list_file, 'r') as file:
                for line in file:
                    title, author, summary = line.strip().split('|')
                    books.append({'title': title, 'author': author, 'summary': summary})
        except FileNotFoundError:
            pass
        return books

    def save_reading_list(self, books: list):
        with open(self.reading_list_file, 'w') as file:
            for book in books:
                file.write(f"{book['title']}|{book['author']}|{book['summary']}\n")