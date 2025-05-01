import json

class FavoritesManager:
    def __init__(self):
        self.favorites = self.load_favorites()

    def save_favorite(self, article: str):
        self.favorites.append(article)
        with open('favorites.txt', 'a') as file:
            file.write(article + "\n")

    def load_favorites(self):
        try:
            with open('favorites.txt', 'r') as file:
                self.favorites = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            self.favorites = []
        return self.favorites