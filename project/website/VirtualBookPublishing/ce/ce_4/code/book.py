class Book:
    def __init__(self, title: str, author: str, content: str):
        self.title = title
        self.author = author
        self.content = content

    def save(self):
        with open('books.txt', 'a') as f:
            f.write(f"{self.title}|{self.author}|{self.content}\n")

    @staticmethod
    def load_all():
        books = []
        try:
            with open('books.txt', 'r') as f:
                for line in f:
                    title, author, content = line.strip().split('|')
                    books.append(Book(title, author, content))
        except FileNotFoundError:
            pass
        return books