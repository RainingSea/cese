class Favorites:
    def __init__(self, user: str):
        self.user = user
        self.favorite_tips = self.load_favorites()

    def add_favorite(self, tip: str) -> None:
        self.favorite_tips.append(tip)
        with open('favorites.txt', 'a') as file:
            file.write(f"{self.user}|{tip}\n")

    def get_favorites(self) -> list:
        return self.favorite_tips

    def load_favorites(self) -> list:
        favorites = []
        with open('favorites.txt', 'r') as file:
            for line in file:
                username, tip = line.strip().split('|')
                if username == self.user:
                    favorites.append(tip)
        return favorites