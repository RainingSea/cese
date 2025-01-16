class Favorites:
    def __init__(self):
        self.favorites = []

    def add(self, destination: str) -> None:
        with open('favorites.txt', 'a') as f:
            f.write(f"{destination}\n")

    def load(self) -> list:
        with open('favorites.txt', 'r') as f:
            return [line.strip() for line in f]