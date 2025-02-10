class ReadingList:
    def __init__(self, username: str):
        self.username = username
        self.list_file = f"{username}_reading_list.txt"

    def add_book(self, book) -> None:
        with open(self.list_file, 'a') as f:
            f.write(f"{book.title}|{book.author}|{book.summary}\n")

    def remove_book(self, book) -> None:
        # Logic to remove a book from the reading list
        pass

    def get_books(self) -> list:
        books = []
        try:
            with open(self.list_file, 'r') as f:
                for line in f:
                    title, author, summary = line.strip().split('|')
                    books.append({'title': title, 'author': author, 'summary': summary})
        except FileNotFoundError:
            pass
        return books