import os

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.book_manager = BookManager()

    def main(self):
        self.user_manager.load_users()
        self.book_manager.load_books()
        self.run()

    def run(self):
        while True:
            print("Welcome to the Online Library Management System")
            choice = input("1: Login\n2: Exit\nChoose an option: ")
            if choice == '1':
                username = input("Username: ")
                password = input("Password: ")
                if self.user_manager.login(username, password):
                    self.dashboard()
                else:
                    print("Invalid credentials!")
            elif choice == '2':
                break

    def dashboard(self):
        while True:
            print("Dashboard")
            choice = input("1: Book Management\n2: User Management\n3: Logout\nChoose an option: ")
            if choice == '1':
                self.book_management()
            elif choice == '2':
                self.user_management()
            elif choice == '3':
                self.user_manager.logout()
                break

    def book_management(self):
        while True:
            choice = input("1: Add Book\n2: Delete Book\n3: View Books\n4: Back\nChoose an option: ")
            if choice == '1':
                title = input("Book Title: ")
                author = input("Book Author: ")
                self.book_manager.add_book(title, author)
            elif choice == '2':
                title = input("Book Title to delete: ")
                self.book_manager.delete_book(title)
            elif choice == '3':
                books = self.book_manager.view_books()
                print("Books in Library:")
                for book in books:
                    print(book)
            elif choice == '4':
                break

    def user_management(self):
        while True:
            choice = input("1: Register User\n2: Back\nChoose an option: ")
            if choice == '1':
                username = input("New Username: ")
                password = input("New Password: ")
                self.user_manager.register(username, password)
            elif choice == '2':
                break

class UserManager:
    def __init__(self):
        self.users = []

    def register(self, username: str, password: str) -> None:
        self.users.append(f"{username}|{password}")
        self.save_users()
        print(f"User {username} registered successfully.")

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            user_info = user.split('|')
            if user_info[0] == username and user_info[1] == password:
                print(f"User {username} logged in successfully.")
                return True
        return False

    def logout(self) -> None:
        print("User logged out.")

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                self.users = [line.strip() for line in file.readlines()]

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user}\n")

class BookManager:
    def __init__(self):
        self.books = []

    def add_book(self, title: str, author: str) -> None:
        self.books.append(f"{title}|{author}")
        self.save_books()
        print(f"Book '{title}' added successfully.")

    def delete_book(self, title: str) -> None:
        self.books = [book for book in self.books if not book.startswith(title + '|')]
        self.save_books()
        print(f"Book '{title}' deleted successfully.")

    def view_books(self) -> list:
        return self.books

    def load_books(self) -> None:
        if os.path.exists('books.txt'):
            with open('books.txt', 'r') as file:
                self.books = [line.strip() for line in file.readlines()]

    def save_books(self) -> None:
        with open('books.txt', 'w') as file:
            for book in self.books:
                file.write(f"{book}\n")

if __name__ == "__main__":
    app = Main()
    app.main()