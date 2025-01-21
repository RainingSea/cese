import json

class DataStorage:
    def save_users(self, data: list) -> None:
        with open('users.txt', 'w') as f:
            for user in data:
                f.write(f"{user['username']}|{user['password']}\n")

    def load_users(self) -> list:
        try:
            with open('users.txt', 'r') as f:
                return [{'username': line.split('|')[0], 'password': line.split('|')[1].strip()} for line in f]
        except FileNotFoundError:
            return []

    def save_books(self, data: list) -> None:
        with open('books.txt', 'w') as f:
            for book in data:
                f.write(json.dumps(book) + '\n')

    def load_books(self) -> list:
        try:
            with open('books.txt', 'r') as f:
                return [json.loads(line) for line in f]
        except FileNotFoundError:
            return []

    def save_reading_list(self, user: str, books: list) -> None:
        with open('reading_list.txt', 'w') as f:
            for book in books:
                f.write(json.dumps(book) + '\n')

    def load_reading_list(self, user: str) -> list:
        try:
            with open('reading_list.txt', 'r') as f:
                return [json.loads(line) for line in f]
        except FileNotFoundError:
            return []