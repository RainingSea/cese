import os

class MovieManager:
    def __init__(self):
        self.movies = {}
        self.favorites = {}

    def load_movies(self):
        if os.path.exists('movies.txt'):
            with open('movies.txt', 'r') as file:
                for line in file:
                    title, details = line.strip().split('|', 1)
                    self.movies[title] = details

    def load_favorites(self, username: str) -> list:
        if username not in self.favorites:
            self.favorites[username] = []
            if os.path.exists('favorites.txt'):
                with open('favorites.txt', 'r') as file:
                    for line in file:
                        user, title = line.strip().split('|')
                        if user == username:
                            self.favorites[username].append(title)
        return self.favorites[username]

    def add_to_favorites(self, username: str, movie_title: str):
        if username not in self.favorites:
            self.favorites[username] = []
        if movie_title not in self.favorites[username]:
            self.favorites[username].append(movie_title)
            self.save_favorites()

    def remove_from_favorites(self, username: str, movie_title: str):
        if username in self.favorites and movie_title in self.favorites[username]:
            self.favorites[username].remove(movie_title)
            self.save_favorites()

    def save_favorites(self):
        with open('favorites.txt', 'w') as file:
            for user, titles in self.favorites.items():
                for title in titles:
                    file.write(f"{user}|{title}\n")

    def search_movies(self, query: str) -> list:
        return [title for title in self.movies if query.lower() in title.lower()]

    def get_movie_details(self, title: str) -> dict:
        return {'title': title, 'details': self.movies.get(title, 'No details available')}