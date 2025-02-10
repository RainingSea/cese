import json

class CultureManager:
    def __init__(self, cultures_file: str, bookmarks_file: str):
        self.cultures_file = cultures_file
        self.bookmarks_file = bookmarks_file
        self.cultures = self.load_cultures()

    def load_cultures(self) -> list:
        cultures = []
        try:
            with open(self.cultures_file, 'r') as file:
                cultures = json.load(file)
        except FileNotFoundError:
            pass
        return cultures

    def get_culture_details(self, culture_name: str) -> dict:
        for culture in self.cultures:
            if culture['name'] == culture_name:
                return culture
        return {}

    def bookmark_fact(self, username: str, culture_name: str) -> bool:
        bookmarks = self.load_bookmarks(username)
        if culture_name not in bookmarks:
            bookmarks.append(culture_name)
            with open(self.bookmarks_file, 'a') as file:
                file.write(f"{username}|{culture_name}\n")
            return True
        return False

    def load_bookmarks(self, username: str) -> list:
        bookmarks = []
        try:
            with open(self.bookmarks_file, 'r') as file:
                for line in file:
                    user, culture_name = line.strip().split('|')
                    if user == username:
                        bookmarks.append(culture_name)
        except FileNotFoundError:
            pass
        return bookmarks