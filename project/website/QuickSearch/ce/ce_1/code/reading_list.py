class ReadingList:
    def __init__(self, filename: str):
        self.filename = filename
        self.reading_lists = self.load_reading_lists()

    def add_to_reading_list(self, username: str, book_title: str) -> bool:
        if username in self.reading_lists:
            if book_title not in self.reading_lists[username]:  # Prevent duplicates
                self.reading_lists[username].append(book_title)
        else:
            self.reading_lists[username] = [book_title]
        self.save_reading_lists()
        return True

    def get_reading_list(self, username: str) -> list:
        return self.reading_lists.get(username, [])

    def load_reading_lists(self) -> dict:
        reading_lists = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, books = line.strip().split('|')
                    reading_lists[username] = books.split(',')
        except FileNotFoundError:
            pass
        return reading_lists

    def save_reading_lists(self):
        with open(self.filename, 'w') as file:
            for username, books in self.reading_lists.items():
                file.write(f"{username}|{','.join(books)}\n")