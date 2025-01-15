import os

class MovieManager:
    def __init__(self):
        self.movies = self.load_movies()
        self.favorites = {}

    def load_movies(self) -> dict:
        if not os.path.exists('movies.txt'):
            return {}
        with open('movies.txt', 'r') as file:
            return {line.split('|')[0]: {'description': line.split('|')[1], 'rating': line.split('|')[2].strip()} for line in file}

    def save_movies(self) -> None:
        with open('movies.txt', 'w') as file:
            for title, details in self.movies.items():
                file.write(f"{title}|{details['description']}|{details['rating']}\n")

    def get_recommendations(self, preferences: list) -> list:
        return list(self.movies.keys())[:5]  # Return first 5 movies as recommendations

    def search_movies(self, query: str) -> list:
        return [title for title in self.movies if query.lower() in title.lower()]

    def get_movie_details(self, title: str) -> dict:
        return self.movies.get(title, {})

    def add_to_favorites(self, username: str, movie_title: str) -> None:
        if username not in self.favorites:
            self.favorites[username] = []
        if movie_title not in self.favorites[username]:
            self.favorites[username].append(movie_title)
            self.save_favorites(username)

    def remove_from_favorites(self, username: str, movie_title: str) -> None:
        if username in self.favorites and movie_title in self.favorites[username]:
            self.favorites[username].remove(movie_title)
            self.save_favorites(username)

    def load_favorites(self, username: str) -> list:
        if os.path.exists('favorites.txt'):
            with open('favorites.txt', 'r') as file:
                for line in file:
                    user, favorites = line.strip().split('|')
                    if user == username:
                        return favorites.split(',')
        return []

    def save_favorites(self, username: str) -> None:
        with open('favorites.txt', 'w') as file:
            for user, favorites in self.favorites.items():
                file.write(f"{user}|{','.join(favorites)}\n")