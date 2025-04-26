class BookmarkManager:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def add_bookmark(self, article_id: str) -> None:
        with open(self.file_path, 'a') as file:
            file.write(f"{article_id}\n")

    def remove_bookmark(self, article_id: str) -> None:
        bookmarks = self.list_bookmarks()
        with open(self.file_path, 'w') as file:
            for bookmark in bookmarks:
                if bookmark != article_id:
                    file.write(f"{bookmark}\n")

    def list_bookmarks(self) -> list:
        with open(self.file_path, 'r') as file:
            return file.read().strip().splitlines()