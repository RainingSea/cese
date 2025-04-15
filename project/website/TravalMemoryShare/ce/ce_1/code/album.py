class Album:
    def __init__(self, title: str, owner: str, is_public: bool):
        self.title = title
        self.owner = owner
        self.photos = []
        self.is_public = is_public

    @staticmethod
    def load_albums() -> list:
        albums = []
        try:
            with open('albums.txt', 'r') as file:
                for line in file:
                    title, owner, is_public = line.strip().split('|')
                    albums.append(Album(title, owner, is_public == 'True'))
        except FileNotFoundError:
            pass
        return albums

    def save(self):
        with open('albums.txt', 'a') as file:
            file.write(f"{self.title}|{self.owner}|{self.is_public}\n")

    def add_photo(self, photo: str):
        self.photos.append(photo)

    def customize_layout(self, layout: str):
        # Implement layout customization logic
        pass