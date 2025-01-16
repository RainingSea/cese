class Comment:
    def __init__(self, album_id: str, user: str, content: str):
        self.album_id = album_id
        self.user = user
        self.content = content

    def save(self):
        pass  # Saving is handled by DataManager