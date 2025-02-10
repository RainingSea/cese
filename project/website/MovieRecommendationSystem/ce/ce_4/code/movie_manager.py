class MovieManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.movies = self.load_movies()

    def load_movies(self) -> dict:
        movies = {}
        try:
            with open(self.filepath, 'r') as file:
                for line in file:
                    movie_id, title, description, rating = line.strip().split('|')
                    movies[movie_id] = {
                        'title': title,
                        'description': description,
                        'rating': rating
                    }
        except FileNotFoundError:
            pass
        return movies

    def get_recommendations(self, user_preferences: dict) -> list:
        # For simplicity, return all movies as recommendations
        return list(self.movies.values())

    def get_movie_details(self, movie_id: str) -> dict:
        return self.movies.get(movie_id, {})