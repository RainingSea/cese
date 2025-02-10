class ReadingList:
    def __init__(self):
        self.user = ''
        self.books = []

    @staticmethod
    def load_reading_list(user: str):
        reading_list = []
        try:
            with open('reading_list.txt', 'r') as file:
                for line in file:
                    username, title = line.strip().split('|')
                    if username == user:
                        reading_list.append(title)
        except FileNotFoundError:
            return []
        return reading_list

    def add_book(self, book: Book):
        with open('reading_list.txt', 'a') as file:
            file.write(f"{self.user}|{book.title}\n")

    def remove_book(self, book: Book):
        # This method would require additional implementation to remove a book.
        pass