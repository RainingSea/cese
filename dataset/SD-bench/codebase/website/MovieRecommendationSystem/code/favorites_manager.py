class FavoritesManager:
    """Manages user favorites for movies."""
    
    def __init__(self, filename: str):
        """Initializes FavoritesManager with a filename to load favorites."""
        self.filename = filename
        self.favorites = self.load_favorites()

    def load_favorites(self) -> dict:
        """Loads favorites from the specified file."""
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

    def add_favorite(self, username: str, movie_title: str) -> bool:
        """Adds a movie to the user's favorites."""
        if username not in self.favorites:
            self.favorites[username] = []
        if movie_title not in self.favorites[username]:
            self.favorites[username].append(movie_title)
            self.save_favorites()
            return True
        return False

    def remove_favorite(self, username: str, movie_title: str) -> bool:
        """Removes a movie from the user's favorites."""
        if username in self.favorites and movie_title in self.favorites[username]:
            self.favorites[username].remove(movie_title)
            self.save_favorites()
            return True
        return False

    def get_favorites(self, username: str) -> list:
        """Retrieves the favorite movies of a user."""
        return self.favorites.get(username, [])

    def save_favorites(self):
        """Saves the current favorites data to the specified file."""
        with open(self.filename, 'w') as file:
            for username, movies in self.favorites.items():
                for movie_title in movies:
                    file.write(f"{username}|{movie_title}\n")