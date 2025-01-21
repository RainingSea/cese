from user import User
from culture import Culture
from bookmark import Bookmark

class CultureFactsApp:
    """Main application class for managing cultures, users, and bookmarks."""
    
    def __init__(self, users_file: str, cultures_file: str, bookmarks_file: str):
        self.users_file = users_file
        self.cultures_file = cultures_file
        self.bookmarks_file = bookmarks_file
        self.cultures = Culture.load_cultures()

    def register(self, username: str, password: str) -> bool:
        """Registers a new user."""
        if User.load(username) is None:
            user = User(username, password)
            user.save()
            return True
        return False

    def login(self, username: str, password: str) -> User:
        """Logs in a user."""
        user = User.load(username)
        if user and user.password == password:
            return user
        return None

    def search_cultures(self, keyword: str) -> list:
        """Searches cultures by keyword."""
        return [culture for culture in self.cultures if keyword.lower() in culture.name.lower()]

    def bookmark_culture(self, user: User, culture_name: str) -> None:
        """Bookmarks a culture for a user."""
        bookmark = Bookmark(user, culture_name)
        bookmark.save()

    def get_bookmarks(self, user: User) -> list:
        """Gets bookmarks for a user."""
        return Bookmark.load_bookmarks(user)

    def remove_bookmark(self, user: User, culture_name: str) -> None:
        """Removes a bookmark for a user."""
        Bookmark.remove_bookmark(user, culture_name)

    def get_culture_details(self, name: str) -> str:
        """Gets details of a specific culture."""
        for culture in self.cultures:
            if culture.name == name:
                return culture.get_details()
        return "Culture not found."