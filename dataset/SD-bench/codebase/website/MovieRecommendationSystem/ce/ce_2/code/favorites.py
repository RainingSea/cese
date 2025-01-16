class Favorites:
    def __init__(self, username: str):
        self.username = username
        self.movies = self.load_favorites()

    def add_movie(self, movie):
        if movie.title not in self.movies:
            self.movies.append(movie.title)
            self.save()

    def remove_movie(self, movie):
        if movie.title in self.movies:
            self.movies.remove(movie.title)
            self.save()

    def get_favorites(self):
        return self.movies

    def load_favorites(self):
        try:
            with open('favorites.txt', 'r') as file:
                return [line.strip() for line in file if line.startswith(self.username)]
        except FileNotFoundError:
            return []

    def save(self):
        with open('favorites.txt', 'w') as file:
            for movie in self.movies:
                file.write(f"{self.username}|{movie}\n")