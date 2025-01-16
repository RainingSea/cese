import os
from user import User
from book import Book

class DataStorage:
    def __init__(self):
        self.users = {}
        self.books = []

    def load_users(self) -> dict:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = User(username, password)
        return self.users

    def load_books(self) -> list:
        if os.path.exists('books.txt'):
            with open('books.txt', 'r') as file:
                for line in file:
                    title, author, summary, cover_image = line.strip().split('|')
                    self.books.append(Book(title, author, summary, cover_image))
        return self.books

    def load_reading_list(self, user: str) -> list:
        reading_list = []
        if os.path.exists('reading_list.txt'):
            with open('reading_list.txt', 'r') as file:
                for line in file:
                    username, book_title = line.strip().split('|')
                    if username == user:
                        reading_list.append(book_title)
        return reading_list

    def save_user(self, user: User) -> None:
        with open('users.txt', 'a') as file:
            file.write(f"{user.username}|{user.password}\n")

    def save_book(self, book: Book) -> None:
        with open('books.txt', 'a') as file:
            file.write(f"{book.title}|{book.author}|{book.summary}|{book.cover_image}\n")

    def save_reading_list(self, user: str, reading_list: 'ReadingList') -> None:
        with open('reading_list.txt', 'a') as file:
            for book in reading_list.get_books():
                file.write(f"{user}|{book.title}\n")