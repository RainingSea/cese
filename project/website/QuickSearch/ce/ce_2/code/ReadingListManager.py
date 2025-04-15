import os
from collections import defaultdict

class ReadingListManager:
    """Manages users' reading lists."""
    
    def __init__(self):
        self.reading_lists = self.load_reading_lists()

    def add_to_reading_list(self, username: str, book_title: str) -> None:
        """Adds a book title to the user's reading list."""
        self.reading_lists[username].append(book_title)
        self.save_reading_lists()

    def get_reading_list(self, username: str) -> list:
        """Retrieves the reading list for a specific user."""
        return self.reading_lists.get(username, [])

    def load_reading_lists(self) -> dict:
        """Loads reading lists from a file into a dictionary."""
        if not os.path.exists('reading_lists.txt'):
            return defaultdict(list)
        reading_lists = defaultdict(list)
        with open('reading_lists.txt', 'r') as file:
            for line in file:
                username, book_title = line.strip().split('|')
                reading_lists[username].append(book_title)
        return reading_lists

    def save_reading_lists(self) -> None:
        """Saves the current reading lists to a file."""
        with open('reading_lists.txt', 'w') as file:
            for username, books in self.reading_lists.items():
                for book in books:
                    file.write(f"{username}|{book}\n")