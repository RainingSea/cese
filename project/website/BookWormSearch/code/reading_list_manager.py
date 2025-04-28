import os

class ReadingListManager:
    def __init__(self, reading_list_file: str):
        self.reading_list_file = reading_list_file
        self.load_reading_lists()

    def load_reading_lists(self):
        self.reading_lists = {}
        if os.path.exists(self.reading_list_file):
            with open(self.reading_list_file, 'r') as file:
                for line in file:
                    username, title = line.strip().split('|')
                    if username not in self.reading_lists:
                        self.reading_lists[username] = []
                    self.reading_lists[username].append(title)

    def add_to_reading_list(self, username: str, book_title: str) -> bool:
        if username not in self.reading_lists:
            self.reading_lists[username] = []
        if book_title not in self.reading_lists[username]:
            self.reading_lists[username].append(book_title)
            with open(self.reading_list_file, 'a') as file:
                file.write(f"{username}|{book_title}\n")
            return True
        return False

    def get_reading_list(self, username: str) -> list:
        return self.reading_lists.get(username, [])

    def remove_from_reading_list(self, username: str, book_title: str) -> bool:
        if username in self.reading_lists and book_title in self.reading_lists[username]:
            self.reading_lists[username].remove(book_title)
            self.save_reading_lists()
            return True
        return False

    def save_reading_lists(self):
        with open(self.reading_list_file, 'w') as file:
            for username, titles in self.reading_lists.items():
                for title in titles:
                    file.write(f"{username}|{title}\n")