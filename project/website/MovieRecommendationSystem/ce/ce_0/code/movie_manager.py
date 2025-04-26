class MovieManager:
    def __init__(self):
        self.movies = []
        self.favorites = {}

    def load_movies(self):
        if os.path.exists('movies.txt'):
            with open('movies.txt', 'r') as file:
                for line in file:
                    title, description, rating = line.strip().split('|')
                    self.movies.append({
                        'title': title,
                        'description': description,
                        'rating': rating
                    })

    def load_favorites(self):
        if os.path.exists('favorites.txt'):
            with open('favorites.txt', 'r') as file:
                for line in file:
                    username, movie_title = line.strip().split('|')
                    if username not in self.favorites:
                        self.favorites[username] = []
                    self.favorites[username].append(movie_title)

    def get_recommendations(self, user_preferences: dict) -> list:
        # Dummy implementation for recommendations
        return self.movies[:5]

    def search_movies(self, query: str) -> list:
        return [movie for movie in self.movies if query.lower() in movie['title'].lower()]

    def get_movie_details(self, title: str) -> dict:
        for movie in self.movies:
            if movie['title'] == title:
                return movie
        return {}

    def add_to_favorites(self, username: str, movie_title: str) -> bool:
        if username not in self.favorites:
            self.favorites[username] = []
        if movie_title in self.favorites[username]:
            return False
        self.favorites[username].append(movie_title)
        with open('favorites.txt', 'a') as file:
            file.write(f"{username}|{movie_title}\n")
        return True

    def get_favorites(self, username: str) -> list:
        return self.favorites.get(username, [])