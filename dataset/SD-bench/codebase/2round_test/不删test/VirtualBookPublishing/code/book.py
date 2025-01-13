class Book:
    def __init__(self, username: str, title: str, author: str, content: str):
        self.username = username
        self.title = title
        self.author = author
        self.content = content

    def save(self):
        with open('books.txt', 'a') as file:
            file.write(f"{self.username}:{self.title}:{self.author}:{self.content}\n")