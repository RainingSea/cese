class Album:
    def __init__(self, user_id: str, title: str, description: str):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.photos = []

    def add_photo(self, photo: str):
        self.photos.append(photo)

    def save(self):
        with open('albums.txt', 'a') as f:
            f.write(f"{self.user_id}|{self.title}|{self.description}|{','.join(self.photos)}\n")