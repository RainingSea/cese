class Bookmark:
    """Represents a bookmark for a culture."""
    
    def __init__(self, user: 'User', culture_name: str):
        self.user = user
        self.culture_name = culture_name

    def save(self) -> None:
        """Saves the bookmark to the bookmarks file."""
        with open('bookmarks.txt', 'a') as f:
            f.write(f"{self.user.username}|{self.culture_name}\n")

    @staticmethod
    def load_bookmarks(user: 'User') -> list:
        """Loads bookmarks for a specific user from the bookmarks file."""
        bookmarks = []
        with open('bookmarks.txt', 'r') as f:
            for line in f:
                bookmark_data = line.strip().split('|')
                if bookmark_data[0] == user.username:
                    bookmarks.append(bookmark_data[1])
        return bookmarks

    @staticmethod
    def remove_bookmark(user: 'User', culture_name: str) -> None:
        """Removes a bookmark for a specific user."""
        bookmarks = []
        with open('bookmarks.txt', 'r') as f:
            for line in f:
                bookmark_data = line.strip().split('|')
                if bookmark_data[0] == user.username and bookmark_data[1] == culture_name:
                    continue
                bookmarks.append(line.strip())
        with open('bookmarks.txt', 'w') as f:
            for bookmark in bookmarks:
                f.write(f"{bookmark}\n")