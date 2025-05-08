class ReadingListManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.reading_list = self.load_reading_list()

    def load_reading_list(self):
        try:
            with open(self.filename, 'r') as file:
                return [line.strip() for line in file]
        except FileNotFoundError:
            return []

    def add_to_reading_list(self, username: str, book_title: str) -> bool:
        if book_title in self.reading_list:
            return False
        self.reading_list.append(book_title)
        with open(self.filename, 'a') as file:
            file.write(f"{book_title}\n")
        return True

    def get_reading_list(self, username: str) -> list:
        return self.reading_list

    def remove_from_reading_list(self, username: str, book_title: str) -> bool:
        if book_title in self.reading_list:
            self.reading_list.remove(book_title)
            with open(self.filename, 'w') as file:
                for title in self.reading_list:
                    file.write(f"{title}\n")
            return True
        return False