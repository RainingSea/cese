class LibrarySystem:
    def __init__(self, users_file='users.txt', books_file='books.txt'):
        self.users_file = users_file
        self.books_file = books_file
        
        # Initialize files if they don't exist
        try:
            with open(self.users_file, 'a+') as f:
                pass
            with open(self.books_file, 'a+') as f:
                pass
        except IOError as e:
            print(f"Error initializing files: {e}")

    def authenticate(self, username, password):
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    stored_user, stored_pass = line.strip().split(',')
                    if stored_user == username and stored_pass == password:
                        return True
            return False
        except IOError:
            return False

    def register_user(self, username, password):
        if self.authenticate(username, password):
            return False  # User already exists
            
        try:
            with open(self.users_file, 'a') as f:
                f.write(f"{username},{password}\n")
            return True
        except IOError:
            return False

    def add_book(self, title, author, isbn):
        try:
            with open(self.books_file, 'a') as f:
                f.write(f"{title},{author},{isbn}\n")
            return True
        except IOError:
            return False

    def delete_book(self, isbn):
        try:
            with open(self.books_file, 'r') as f:
                lines = f.readlines()
            
            with open(self.books_file, 'w') as f:
                deleted = False
                for line in lines:
                    _, _, current_isbn = line.strip().split(',')
                    if current_isbn != isbn:
                        f.write(line)
                    else:
                        deleted = True
                return deleted
        except IOError:
            return False

    def list_books(self):
        books = []
        try:
            with open(self.books_file, 'r') as f:
                for line in f:
                    title, author, isbn = line.strip().split(',')
                    books.append({'title': title, 'author': author, 'isbn': isbn})
        except IOError:
            pass
        return books

    def list_users(self):
        users = []
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    username, password = line.strip().split(',')
                    users.append({'username': username, 'password': password})
        except IOError:
            pass
        return users

    def search_books(self, query):
        query = query.lower()
        results = []
        try:
            with open(self.books_file, 'r') as f:
                for line in f:
                    title, author, isbn = line.strip().split(',')
                    if (query in title.lower() or 
                        query in author.lower() or 
                        query in isbn.lower()):
                        results.append({'title': title, 'author': author, 'isbn': isbn})
        except IOError:
            pass
        return results