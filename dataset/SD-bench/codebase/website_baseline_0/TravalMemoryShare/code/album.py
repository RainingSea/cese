class Album:
    def __init__(self, title: str, photos: list, is_public: bool):
        self.title = title
        self.photos = photos
        self.is_public = is_public

    def create_album(self) -> bool:
        with open('albums.txt', 'a') as file:
            file.write(f"{self.title}|{','.join(self.photos)}|{self.is_public}\n")
        return True

    def customize_layout(self) -> bool:
        # Layout customization logic can be added here
        return True

    def share_album(self) -> bool:
        # Sharing logic can be implemented here
        return True