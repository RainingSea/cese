class LibrarySystem:
    def __init__(self, users_file='users.txt', books_file='books.txt'):
        self.users_file = users_file
        self.books_file = books_file

    def register_user(self, username, password, role):
        with open(self.users_file, 'a') as f:
            f.write(f"{username}:{password}:{role}\n")

    def authenticate_user(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 3 and parts[0] == username and parts[1] == password:
                    return True
        return False

    def add_book(self, title, author, isbn):
        with open(self.books_file, 'a') as f:
            f.write(f"{title}:{author}:{isbn}:available\n")

    def delete_book(self, isbn):
        books = []
        with open(self.books_file, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 4 and parts[2] != isbn:
                    books.append(line)
        
        with open(self.books_file, 'w') as f:
            f.writelines(books)

    def search_books(self, query):
        results = []
        with open(self.books_file, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 4 and (query.lower() in parts[0].lower() or query.lower() in parts[1].lower()):
                    results.append({'title': parts[0], 'author': parts[1], 'isbn': parts[2], 'status': parts[3]})
        return results

    def list_books(self):
        books = []
        with open(self.books_file, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 4:
                    books.append({'title': parts[0], 'author': parts[1], 'isbn': parts[2], 'status': parts[3]})
        return books

    def list_users(self):
        users = []
        with open(self.users_file, 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) == 3:
                    users.append({'username': parts[0], 'role': parts[2]})
        return users