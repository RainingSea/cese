class MovieManager:
    def __init__(self):
        self.movies = []
        self.favorites = []

    def search_movies(self, query: str) -> list:
        return [movie for movie in self.movies if query.lower() in movie['title'].lower()]

    def get_recommendations(self, preferences: dict) -> list:
        # Simple recommendation logic based on preferences
        return self.movies[:5]  # Return first 5 movies as a placeholder

    def load_movies(self) -> list:
        try:
            with open('movies.txt', 'r') as file:
                for line in file:
                    title, genre, year = line.strip().split('|')
                    self.movies.append({'title': title, 'genre': genre, 'year': year})
        except FileNotFoundError:
            pass

    def add_to_favorites(self, movie_id: str) -> bool:
        if movie_id not in self.favorites:
            self.favorites.append(movie_id)
            self.save_favorites()
            return True
        return False

    def remove_from_favorites(self, movie_id: str) -> bool:
        if movie_id in self.favorites:
            self.favorites.remove(movie_id)
            self.save_favorites()
            return True
        return False

    def save_favorites(self):
        with open('favorites.txt', 'w') as file:
            for movie_id in self.favorites:
                file.write(f"{movie_id}\n")