class FavoritesManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.favorites = self.load_favorites()

    def add_favorite(self, username: str, movie_title: str) -> bool:
        if username not in self.favorites:
            self.favorites[username] = []
        if movie_title in self.favorites[username]:
            return False
        self.favorites[username].append(movie_title)
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{movie_title}\n")
        return True

    def remove_favorite(self, username: str, movie_title: str) -> bool:
        if username in self.favorites and movie_title in self.favorites[username]:
            self.favorites[username].remove(movie_title)
            self.save_favorites()
            return True
        return False

    def get_favorites(self, username: str) -> list:
        return self.favorites.get(username, [])

    def load_favorites(self) -> dict:
        favorites = {}
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, movie_title = line.strip().split('|')
                    if username not in favorites:
                        favorites[username] = []
                    favorites[username].append(movie_title)
        except FileNotFoundError:
            pass
        return favorites

    def save_favorites(self):
        with open(self.filename, 'w') as file:
            for username, movies in self.favorites.items():
                for movie in movies:
                    file.write(f"{username}|{movie}\n")