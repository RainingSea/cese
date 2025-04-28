class MovieManager:
    def __init__(self):
        self.movies = {}
        self.favorites = {}

    def load_movies(self):
        with open('movies.txt', 'r') as file:
            for line in file:
                title, description, rating = line.strip().split('|')
                self.movies[title] = {'description': description, 'rating': rating}

    def load_favorites(self):
        with open('favorites.txt', 'r') as file:
            for line in file:
                username, movie_title = line.strip().split('|')
                if username not in self.favorites:
                    self.favorites[username] = []
                self.favorites[username].append(movie_title)

    def search_movies(self, query: str) -> list:
        return [title for title in self.movies if query.lower() in title.lower()]

    def get_movie_details(self, title: str) -> dict:
        return self.movies.get(title, {})

    def add_to_favorites(self, username: str, movie_title: str) -> None:
        if username not in self.favorites:
            self.favorites[username] = []
        if movie_title not in self.favorites[username]:
            self.favorites[username].append(movie_title)
            with open('favorites.txt', 'a') as file:
                file.write(f"{username}|{movie_title}\n")

    def remove_from_favorites(self, username: str, movie_title: str) -> None:
        if username in self.favorites and movie_title in self.favorites[username]:
            self.favorites[username].remove(movie_title)
            self.save_favorites()

    def save_favorites(self):
        with open('favorites.txt', 'w') as file:
            for username, movies in self.favorites.items():
                for movie in movies:
                    file.write(f"{username}|{movie}\n")