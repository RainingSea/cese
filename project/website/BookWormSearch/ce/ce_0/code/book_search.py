class BookSearch:
    def __init__(self, books_file):
        self.books_file = books_file
        self.load_books()

    def load_books(self):
        self.books = {}
        with open(self.books_file, 'r') as file:
            for line in file:
                title, author, summary, description = line.strip().split('|')
                self.books[title] = {
                    'author': author,
                    'summary': summary,
                    'description': description
                }

    def search_books(self, query: str) -> list:
        results = []
        for title, info in self.books.items():
            if query.lower() in title.lower():
                results.append({'title': title, 'author': info['author'], 'summary': info['summary']})
        return results

    def get_book_details(self, title: str):
        return self.books.get(title)