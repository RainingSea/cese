class MovieManager:
    def __init__(self):
        self.movies = []

    def load_movies(self) -> None:
        if os.path.exists('movies.txt'):
            with open('movies.txt', 'r') as file:
                self.movies = [line.strip().split('|') for line in file.readlines()]

    def get_recommendations(self, preferences: list) -> list:
        # Dummy implementation for recommendations
        return self.movies[:5]  # Return first 5 movies as recommendations

    def search_movies(self, query: str) -> list:
        return [movie for movie in self.movies if query.lower() in movie[0].lower()]

    def load_favorites(self, username: str) -> list:
        favorites = []
        if os.path.exists('favorites.txt'):
            with open('favorites.txt', 'r') as file:
                for line in file:
                    user, fav_movie = line.strip().split('|')
                    if user == username:
                        favorites.append(fav_movie)
        return favorites

    def save_favorites(self, username: str, favorites: list) -> None:
        with open('favorites.txt', 'a') as file:
            for movie in favorites:
                file.write(f"{username}|{movie}\n")