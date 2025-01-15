class MovieManager:
    """Manages movie data and recommendations."""
    
    def __init__(self, filename: str):
        """Initializes MovieManager with a filename to load movies."""
        self.filename = filename
        self.movies = self.load_movies()

    def load_movies(self) -> list:
        """Loads movies from the specified file."""
        movies = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    title, genre, year = line.strip().split('|')
                    movies.append({'title': title, 'genre': genre, 'year': year})
        except FileNotFoundError:
            pass
        return movies

    def search_movies(self, query: str) -> list:
        """Searches for movies that match the query."""
        return [movie for movie in self.movies if query.lower() in movie['title'].lower()]

    def get_movie_details(self, title: str) -> dict:
        """Retrieves the details of a specific movie."""
        for movie in self.movies:
            if movie['title'] == title:
                return movie
        return {}

    def get_recommendations(self) -> list:
        """Retrieves a list of recommended movies."""
        return self.movies