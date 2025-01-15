class MovieManager:
    def __init__(self):
        self.movies = self.load_movies()

    def load_movies(self) -> dict:
        movies = {}
        try:
            with open('movies.txt', 'r') as file:
                for line in file:
                    movie_id, title, genre = line.strip().split('|')
                    movies[movie_id] = {'title': title, 'genre': genre}
        except FileNotFoundError:
            pass
        return movies

    def get_recommendations(self, user_preferences: list) -> list:
        recommendations = []
        for movie in self.movies.values():
            if movie['genre'] in user_preferences:
                recommendations.append(movie)
        return recommendations

    def search_movies(self, query: str) -> list:
        return [movie for movie in self.movies.values() if query.lower() in movie['title'].lower()]

    def get_movie_details(self, movie_id: str) -> dict:
        return self.movies.get(movie_id, {})