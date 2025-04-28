import os
import json

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.book_manager = BookManager()
        self.session_manager = SessionManager()

    def main(self):
        self.load_data()
        # Here you would typically start your web server or main loop
        print("Online Library Management System started.")

    def load_data(self):
        self.user_manager.load_users()
        self.book_manager.load_books()
        self.session_manager.load_sessions()

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
        if any(user['username'] == username for user in self.users):
            return False
        self.users.append({'username': username, 'password': password})
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        if any(user['username'] == username and user['password'] == password for user in self.users):
            self.session_manager.create_session(username)
            return True
        return False

    def logout(self, username: str) -> None:
        self.session_manager.end_session(username)

    def view_users(self) -> list:
        return self.users

class BookManager:
    def __init__(self):
        self.books = []

    def load_books(self):
        if os.path.exists('books.txt'):
            with open('books.txt', 'r') as file:
                for line in file:
                    title, author = line.strip().split('|')
                    self.books.append({'title': title, 'author': author})

    def add_book(self, title: str, author: str) -> bool:
        if any(book['title'] == title for book in self.books):
            return False
        self.books.append({'title': title, 'author': author})
        with open('books.txt', 'a') as file:
            file.write(f"{title}|{author}\n")
        return True

    def delete_book(self, title: str) -> bool:
        for book in self.books:
            if book['title'] == title:
                self.books.remove(book)
                self.save_books()
                return True
        return False

    def save_books(self):
        with open('books.txt', 'w') as file:
            for book in self.books:
                file.write(f"{book['title']}|{book['author']}\n")

    def view_books(self) -> list:
        return self.books

    def search_books(self, query: str) -> list:
        return [book for book in self.books if query.lower() in book['title'].lower()]

class SessionManager:
    def __init__(self):
        self.sessions = {}

    def load_sessions(self):
        if os.path.exists('sessions.txt'):
            with open('sessions.txt', 'r') as file:
                for line in file:
                    username = line.strip()
                    self.sessions[username] = True

    def create_session(self, username: str) -> None:
        self.sessions[username] = True
        with open('sessions.txt', 'a') as file:
            file.write(f"{username}\n")

    def end_session(self, username: str) -> None:
        if username in self.sessions:
            del self.sessions[username]
            self.save_sessions()

    def save_sessions(self):
        with open('sessions.txt', 'w') as file:
            for username in self.sessions.keys():
                file.write(f"{username}\n")

if __name__ == "__main__":
    app = Main()
    app.main()