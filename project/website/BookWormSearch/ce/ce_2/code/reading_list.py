class ReadingList:
    def __init__(self, username: str):
        self.username = username
        self.books = []

    def add_book(self, book_id: str) -> None:
        self.books.append(book_id)
        self.save_reading_list()

    def remove_book(self, book_id: str) -> None:
        self.books.remove(book_id)
        self.save_reading_list()

    def load_reading_list(self) -> list:
        try:
            with open('reading_lists.txt', 'r') as f:
                for line in f:
                    user, books = line.strip().split('|')
                    if user == self.username:
                        self.books = books.split(',')
                        break
        except FileNotFoundError:
            pass
        return self.books

    def save_reading_list(self) -> None:
        lines = []
        try:
            with open('reading_lists.txt', 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            pass

        updated = False
        for i in range(len(lines)):
            if lines[i].startswith(self.username):
                lines[i] = f"{self.username}|{','.join(self.books)}\n"
                updated = True
                break

        if not updated:
            lines.append(f"{self.username}|{','.join(self.books)}\n")

        with open('reading_lists.txt', 'w') as f:
            f.writelines(lines)