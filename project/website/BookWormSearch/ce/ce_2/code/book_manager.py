class BookManager:
    def __init__(self):
        self.books = self.load_books()

    def load_books(self):
        books = []
        with open('books.txt', 'r') as file:
            for line in file:
                title, author, summary, description = line.strip().split(',')
                books.append({
                    'title': title,
                    'author': author,
                    'summary': summary,
                    'description': description
                })
        return books

    def search_books(self, query: str):
        results = []
        for book in self.books:
            if query.lower() in book['title'].lower() or query.lower() in book['author'].lower():
                results.append(book)
        return results

    def get_book_details(self, title: str):
        for book in self.books:
            if book['title'] == title:
                return book
        return None