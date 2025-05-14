class Movie:
    def __init__(self, id, title, description, rating, genres):
        self.id = id
        self.title = title
        self.description = description
        self.rating = rating
        self.genres = genres

class MovieManager:
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.movies_file = 'movies.txt'
        self.favorites_file = 'favorites.txt'

    def load_movies(self):
        movies = []
        lines = self.file_handler.read_file(self.movies_file)
        for line in lines:
            parts = line.split('|')
            if len(parts) >= 5:
                try:
                    movies.append(Movie(
                        id=parts[0].strip(),
                        title=parts[1].strip(),
                        description=parts[2].strip(),
                        rating=float(parts[3].strip()),
                        genres=[g.strip() for g in parts[4].split(',')]
                    ))
                except (ValueError, IndexError):
                    continue
        return sorted(movies, key=lambda x: x.rating, reverse=True)

    def search(self, query):
        if not query:
            return []
        movies = self.load_movies()
        return [movie for movie in movies if query.lower() in movie.title.lower()]

    def get_recommendations(self, username):
        favorites = self.get_favorites(username)
        favorite_genres = set()
        
        for movie in self.load_movies():
            if movie.id in [fav.id for fav in favorites]:
                favorite_genres.update(movie.genres)
        
        recommendations = []
        for movie in self.load_movies():
            if movie.id not in [fav.id for fav in favorites] and set(movie.genres).intersection(favorite_genres):
                recommendations.append(movie)
        
        return recommendations[:5] if recommendations else self.load_movies()[:5]

    def add_favorite(self, username, movie_id):
        if not self.get_movie_details(movie_id):
            return False
            
        favorites = self.file_handler.read_file(self.favorites_file)
        new_favorite = f"{username}|{movie_id}"
        if new_favorite not in favorites:
            favorites.append(new_favorite)
            self.file_handler.write_file(self.favorites_file, favorites)
            return True
        return False

    def remove_favorite(self, username, movie_id):
        favorites = self.file_handler.read_file(self.favorites_file)
        new_favorites = [fav for fav in favorites if fav != f"{username}|{movie_id}"]
        if len(new_favorites) != len(favorites):
            self.file_handler.write_file(self.favorites_file, new_favorites)
            return True
        return False

    def get_movie_details(self, movie_id):
        for movie in self.load_movies():
            if movie.id == movie_id:
                return movie
        return None

    def get_favorites(self, username):
        favorites = self.file_handler.read_file(self.favorites_file)
        favorite_ids = []
        for fav in favorites:
            parts = fav.split('|')
            if len(parts) == 2 and parts[0] == username:
                favorite_ids.append(parts[1])
        
        movies = self.load_movies()
        return [movie for movie in movies if movie.id in favorite_ids]