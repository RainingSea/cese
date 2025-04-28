import os
import json

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.book_manager = BookManager()

    def main(self):
        # Load existing data
        self.user_manager.load_users()
        self.book_manager.load_books()
        # Start application (placeholder for actual web framework routing)
        print("Welcome to the Online Library Management System")

class UserManager:
    def __init__(self):
        self.users = []

    def load_users(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users.append({'username': username, 'password': password})

    def register(self, username: str, password: str) -> bool:
        self.users.append({'username': username, 'password': password})
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                self.start_session(username)
                return True
        return False

    def logout(self, username: str) -> None:
        self.end_session(username)

    def view_users(self) -> list:
        return self.users

    def start_session(self, username: str) -> None:
        with open('sessions.txt', 'a') as file:
            file.write(f"{username}\n")

    def end_session(self, username: str) -> None:
        # Placeholder for session management logic
        pass

class BookManager:
    def __init__(self):
        self.books = []

    def load_books(self):
        if os.path.exists('books.txt'):
            with open('books.txt', 'r') as file:
                for line in file:
                    title, author, isbn = line.strip().split('|')
                    self.books.append({'title': title, 'author': author, 'isbn': isbn})

    def add_book(self, title: str, author: str, isbn: str) -> bool:
        self.books.append({'title': title, 'author': author, 'isbn': isbn})
        with open('books.txt', 'a') as file:
            file.write(f"{title}|{author}|{isbn}\n")
        return True

    def delete_book(self, isbn: str) -> bool:
        self.books = [book for book in self.books if book['isbn'] != isbn]
        self.save_books()
        return True

    def save_books(self) -> None:
        with open('books.txt', 'w') as file:
            for book in self.books:
                file.write(f"{book['title']}|{book['author']}|{book['isbn']}\n")

    def view_books(self) -> list:
        return self.books

    def search_books(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book['title'].lower() or query.lower() in book['author'].lower()]

if __name__ == "__main__":
    app = Main()
    app.main()