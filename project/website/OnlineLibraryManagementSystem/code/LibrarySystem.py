from BookManager import BookManager
from UserManager import UserManager

class LibrarySystem:
    def __init__(self):
        self.book_manager = BookManager('books.txt')
        self.user_manager = UserManager('users.txt')
        self.current_user = None

    def login(self, username, password):
        if self.user_manager.validate_user(username, password):
            self.current_user = username
            return True
        return False

    def logout(self):
        self.current_user = None

    def get_current_user(self):
        return self.current_user

    def get_stats(self):
        return {
            'book_count': len(self.book_manager.list_books()),
            'user_count': len(self.user_manager.list_users())
        }