class MovieManager:
    def __init__(self):
        self.movies = self.load_movies()
        self.favorites = {}

    def load_movies(self) -> dict:
        movies = {}
        try:
            with open('movies.txt', 'r') as file:
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

    def save_movies(self) -> None:
        with open('movies.txt', 'w') as file:
            for movie_id, details in self.movies.items():
                file.write(f"{movie_id}|{details['title']}|{details['description']}|{details['rating']}\n")

    def get_recommendations(self, user: str) -> list:
        return self.favorites.get(user, [])

    def search_movies(self, query: str) -> list:
        return [movie for movie in self.movies.values() if query.lower() in movie['title'].lower()]

    def get_movie_details(self, movie_id: str) -> dict:
        return self.movies.get(movie_id, {})

    def add_to_favorites(self, user: str, movie_id: str) -> None:
        if user not in self.favorites:
            self.favorites[user] = []
        if movie_id not in self.favorites[user]:
            self.favorites[user].append(movie_id)
            self.save_favorites(user)

    def remove_from_favorites(self, user: str, movie_id: str) -> None:
        if user in self.favorites and movie_id in self.favorites[user]:
            self.favorites[user].remove(movie_id)
            self.save_favorites(user)

    def load_favorites(self, user: str) -> list:
        try:
            with open('favorites.txt', 'r') as file:
                for line in file:
                    username, movie_ids = line.strip().split('|')
                    if username == user:
                        return movie_ids.split(',')
        except FileNotFoundError:
            return []
        return []

    def save_favorites(self, user: str) -> None:
        with open('favorites.txt', 'w') as file:
            for username, movie_ids in self.favorites.items():
                file.write(f"{username}|{','.join(movie_ids)}\n")