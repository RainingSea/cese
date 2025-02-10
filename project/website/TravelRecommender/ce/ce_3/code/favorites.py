class Favorites:
    def __init__(self, username: str):
        self.username = username
        self.favorite_destinations = []

    def save_favorite(self, destination: str):
        self.favorite_destinations.append(destination)

    def load_favorites(self):
        return self.favorite_destinations