import os

class ReadingListManager:
    """Manages users' reading lists."""
    reading_list_file = 'reading_list.txt'

    def __init__(self):
        """Initialize ReadingListManager and load reading lists from file."""
        self.reading_lists = self.load_reading_lists()

    def load_reading_lists(self) -> dict:
        """Load reading lists from a file."""
        reading_lists = {}
        try:
            with open(self.reading_list_file, 'r') as file:
                for line in file:
                    username, books = line.strip().split('|')
                    reading_lists[username] = books.split(',')
        except FileNotFoundError:
            pass
        return reading_lists

    def add_to_reading_list(self, username: str, book_title: str) -> None:
        """Add a book to the user's reading list."""
        if username in self.reading_lists:
            if book_title not in self.reading_lists[username]:
                self.reading_lists[username].append(book_title)
        else:
            self.reading_lists[username] = [book_title]
        self.save_reading_lists()

    def get_reading_list(self, username: str) -> list:
        """Get the reading list for a user."""
        return self.reading_lists.get(username, [])

    def save_reading_lists(self) -> None:
        """Save reading lists to a file."""
        with open(self.reading_list_file, 'w') as file:
            for username, books in self.reading_lists.items():
                file.write(f"{username}|{','.join(books)}\n")