class FavoritesManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.favorites = self.load_favorites()

    def add_favorite(self, user_id: str, movie_id: str) -> None:
        if user_id not in self.favorites:
            self.favorites[user_id] = []
        if movie_id not in self.favorites[user_id]:
            self.favorites[user_id].append(movie_id)
            self.save_favorites()

    def remove_favorite(self, user_id: str, movie_id: str) -> None:
        if user_id in self.favorites and movie_id in self.favorites[user_id]:
            self.favorites[user_id].remove(movie_id)
            self.save_favorites()

    def get_favorites(self, user_id: str) -> list:
        return self.favorites.get(user_id, [])

    def load_favorites(self) -> dict:
        favorites = {}
        try:
            with open(self.filepath, 'r') as file:
                for line in file:
                    user_id, movie_id = line.strip().split('|')
                    if user_id not in favorites:
                        favorites[user_id] = []
                    favorites[user_id].append(movie_id)
        except FileNotFoundError:
            pass
        return favorites

    def save_favorites(self) -> None:
        with open(self.filepath, 'w') as file:
            for user_id, movie_ids in self.favorites.items():
                for movie_id in movie_ids:
                    file.write(f"{user_id}|{movie_id}\n")