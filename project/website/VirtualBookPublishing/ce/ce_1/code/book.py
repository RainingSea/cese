class Book:
    def __init__(self, username: str, title: str, author: str, content: str):
        self.username = username
        self.title = title
        self.author = author
        self.content = content

    def save(self):
        with open('books.txt', 'a') as file:
            file.write(f"{self.username}:{self.title}:{self.author}:{self.content}\n")

    @staticmethod
    def load_books() -> list:
        books = []
        try:
            with open('books.txt', 'r') as file:
                for line in file:
                    username, title, author, content = line.strip().split(':')
                    books.append(Book(username, title, author, content))
        except FileNotFoundError:
            pass
        return books