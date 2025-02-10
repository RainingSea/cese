class MovieManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.movies = self.load_movies()

    def load_movies(self) -> list:
        movies = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    title, genre, year = line.strip().split('|')
                    movies.append({'title': title, 'genre': genre, 'year': year})
        except FileNotFoundError:
            pass
        return movies

    def get_recommendations(self, preferences: dict) -> list:
        recommendations = []
        for movie in self.movies:
            if movie['genre'] in preferences.get('genres', []):
                recommendations.append(movie)
        return recommendations

    def get_movie_details(self, title: str) -> dict:
        for movie in self.movies:
            if movie['title'] == title:
                return movie
        return {}