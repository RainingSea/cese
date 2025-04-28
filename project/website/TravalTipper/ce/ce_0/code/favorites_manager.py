class FavoritesManager:
    def __init__(self):
        self.favorites = []
        self.load_favorites()

    def save_favorite(self, tip: str) -> None:
        self.favorites.append(tip)
        self.save_favorites()

    def load_favorites(self) -> None:
        try:
            with open('favorites.txt', 'r') as file:
                self.favorites = [line.strip() for line in file]
        except FileNotFoundError:
            self.favorites = []

    def save_favorites(self) -> None:
        with open('favorites.txt', 'w') as file:
            for tip in self.favorites:
                file.write(f"{tip}\n")