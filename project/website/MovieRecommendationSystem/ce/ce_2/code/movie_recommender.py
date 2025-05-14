from werkzeug.security import generate_password_hash, check_password_hash

class MovieRecommender:
    def __init__(self, users_file='users.txt', movies_file='movies.txt', favorites_file='favorites.txt'):
        self.users_file = users_file
        self.movies_file = movies_file
        self.favorites_file = favorites_file

    def register_user(self, username, password):
        with open(self.users_file, 'a+') as f:
            f.seek(0)
            for line in f:
                if line.startswith(username + '|'):
                    return False
            f.write(f"{username}|{password}\n")
        return True

    def login_user(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_username, stored_password = line.strip().split('|')
                if stored_username == username and stored_password == password:
                    return True
        return False

    def get_recommendations(self, username):
        favorites = self.get_favorites(username)
        favorite_genres = set()
        
        # Get genres from favorite movies
        with open(self.movies_file, 'r') as f:
            for line in f:
                title, _, _, genres = line.strip().split('|')
                if title in favorites:
                    favorite_genres.update(genres.split(','))
        
        # Recommend movies with matching genres
        recommendations = []
        with open(self.movies_file, 'r') as f:
            for line in f:
                title, description, rating, genres = line.strip().split('|')
                if title not in favorites and any(genre in favorite_genres for genre in genres.split(',')):
                    recommendations.append({
                        'title': title,
                        'description': description,
                        'rating': rating,
                        'genres': genres
                    })
        
        return recommendations if recommendations else self.get_all_movies()

    def get_all_movies(self):
        movies = []
        with open(self.movies_file, 'r') as f:
            for line in f:
                title, description, rating, genres = line.strip().split('|')
                movies.append({
                    'title': title,
                    'description': description,
                    'rating': rating,
                    'genres': genres
                })
        return movies

    def search_movies(self, query):
        results = []
        with open(self.movies_file, 'r') as f:
            for line in f:
                title, description, rating, genres = line.strip().split('|')
                if query.lower() in title.lower() or query.lower() in description.lower():
                    results.append({
                        'title': title,
                        'description': description,
                        'rating': rating,
                        'genres': genres
                    })
        return results

    def get_movie_details(self, title):
        with open(self.movies_file, 'r') as f:
            for line in f:
                movie_title, description, rating, genres = line.strip().split('|')
                if movie_title == title:
                    return {
                        'title': movie_title,
                        'description': description,
                        'rating': rating,
                        'genres': genres
                    }
        return None

    def add_favorite(self, username, movie_title):
        with open(self.favorites_file, 'a+') as f:
            f.seek(0)
            for line in f:
                if line.strip() == f"{username}|{movie_title}":
                    return False
            f.write(f"{username}|{movie_title}\n")
        return True

    def remove_favorite(self, username, movie_title):
        lines = []
        removed = False
        with open(self.favorites_file, 'r') as f:
            for line in f:
                if line.strip() != f"{username}|{movie_title}":
                    lines.append(line)
                else:
                    removed = True
        
        if removed:
            with open(self.favorites_file, 'w') as f:
                f.writelines(lines)
        return removed

    def get_favorites(self, username):
        favorites = []
        with open(self.favorites_file, 'r') as f:
            for line in f:
                user, movie = line.strip().split('|')
                if user == username:
                    favorites.append(movie)
        return favorites