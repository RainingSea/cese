import os

class UserManager:
    def __init__(self):
        self.users = {}

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")


class BookManager:
    def __init__(self):
        self.books = []

    def search_books(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book['title'].lower()]

    def load_books(self) -> None:
        if os.path.exists('books.txt'):
            with open('books.txt', 'r') as file:
                for line in file:
                    title, author, summary, cover_image, description = line.strip().split('|')
                    self.books.append({
                        'title': title,
                        'author': author,
                        'summary': summary,
                        'cover_image': cover_image,
                        'description': description
                    })


class ReadingList:
    def __init__(self):
        self.reading_list = {}

    def add_to_reading_list(self, username: str, book_id: str) -> None:
        if username not in self.reading_list:
            self.reading_list[username] = []
        self.reading_list[username].append(book_id)
        self.save_reading_list()

    def load_reading_list(self) -> None:
        if os.path.exists('reading_list.txt'):
            with open('reading_list.txt', 'r') as file:
                for line in file:
                    username, book_id = line.strip().split('|')
                    if username not in self.reading_list:
                        self.reading_list[username] = []
                    self.reading_list[username].append(book_id)

    def save_reading_list(self) -> None:
        with open('reading_list.txt', 'w') as file:
            for username, books in self.reading_list.items():
                for book_id in books:
                    file.write(f"{username}|{book_id}\n")