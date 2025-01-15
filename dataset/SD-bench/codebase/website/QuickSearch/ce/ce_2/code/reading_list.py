class ReadingList:
    def __init__(self, user: str):
        self.user = user
        self.books = self.load_reading_list('reading_list.txt')

    def load_reading_list(self, file_path: str) -> list:
        books = []
        with open(file_path, 'r') as file:
            for line in file:
                username, book_title = line.strip().split('|')
                if username == self.user:
                    books.append(book_title)
        return books

    def add_book(self, book_title: str) -> bool:
        with open('reading_list.txt', 'a') as file:
            file.write(f"{self.user}|{book_title}\n")
        return True

    def get_reading_list(self) -> list:
        return self.books