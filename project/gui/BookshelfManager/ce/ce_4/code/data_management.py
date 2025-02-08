import os

def load_books_from_file(file_path='books.txt') -> list:
    books = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                title, author, genre, year, notes, rating = line.strip().split(',')
                books.append(Book(title, author, genre, int(year), notes, float(rating)))
    return books

def save_books_to_file(books, file_path='books.txt') -> None:
    with open(file_path, 'w') as file:
        for book in books:
            file.write(f"{book.title},{book.author},{book.genre},{book.year},{book.notes},{book.rating}\n")