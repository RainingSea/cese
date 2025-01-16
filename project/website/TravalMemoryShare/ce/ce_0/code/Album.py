class Album:
    def __init__(self, title: str, user: str, images: list, is_public: bool):
        self.title = title
        self.user = user
        self.images = images
        self.is_public = is_public

    def save(self):
        pass  # Saving is handled by DataManager