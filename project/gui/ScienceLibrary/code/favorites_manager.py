import json

class FavoritesManager:
    def __init__(self):
        self.favorites = []

    def load_favorites(self):
        try:
            with open('favorites.json', 'r') as file:
                self.favorites = json.load(file)
        except FileNotFoundError:
            self.favorites = []

    def add_favorite(self, article: str) -> None:
        if article not in self.favorites:
            self.favorites.append(article)
            self.save_favorites()

    def remove_favorite(self, article: str) -> None:
        if article in self.favorites:
            self.favorites.remove(article)
            self.save_favorites()

    def save_favorites(self) -> None:
        with open('favorites.json', 'w') as file:
            json.dump(self.favorites, file, indent=4)

    def organize_favorites(self) -> None:
        # Example organization: sort by title
        self.favorites.sort()
        self.save_favorites()