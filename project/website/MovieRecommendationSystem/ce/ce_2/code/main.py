import os
import json

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.movie_manager = MovieManager()
        self.user_manager.load_users()
        self.movie_manager.load_movies()
        self.movie_manager.load_favorites()

    def main(self):
        # Placeholder for the main application logic
        print("Welcome to the Movie Recommendation App")

class UserManager:
    def __init__(self):
        self.users = []

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append((username, password))
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user[0] == username and user[1] == password for user in self.users)

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                self.users = [line.strip().split('|') for line in file.readlines()]

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')

class MovieManager:
    def __init__(self):
        self.movies = []
        self.favorites = {}

    def search_movies(self, query: str) -> list:
        return [movie for movie in self.movies if query.lower() in movie[1].lower()]

    def get_movie_details(self, movie_id: str) -> dict:
        for movie in self.movies:
            if movie[0] == movie_id:
                return {'id': movie[0], 'title': movie[1], 'description': movie[2], 'rating': movie[3]}
        return {}

    def add_to_favorites(self, user_id: str, movie_id: str) -> None:
        if user_id in self.favorites:
            self.favorites[user_id].add(movie_id)
        else:
            self.favorites[user_id] = {movie_id}
        self.save_favorites()

    def remove_from_favorites(self, user_id: str, movie_id: str) -> None:
        if user_id in self.favorites and movie_id in self.favorites[user_id]:
            self.favorites[user_id].remove(movie_id)
            self.save_favorites()

    def load_movies(self) -> None:
        if os.path.exists('movies.txt'):
            with open('movies.txt', 'r') as file:
                self.movies = [line.strip().split('|') for line in file.readlines()]

    def save_movies(self) -> None:
        with open('movies.txt', 'w') as file:
            for movie in self.movies:
                file.write('|'.join(movie) + '\n')

    def load_favorites(self) -> None:
        if os.path.exists('favorites.txt'):
            with open('favorites.txt', 'r') as file:
                for line in file:
                    user_id, movie_id = line.strip().split('|')
                    if user_id in self.favorites:
                        self.favorites[user_id].add(movie_id)
                    else:
                        self.favorites[user_id] = {movie_id}

    def save_favorites(self) -> None:
        with open('favorites.txt', 'w') as file:
            for user_id, movie_ids in self.favorites.items():
                for movie_id in movie_ids:
                    file.write(f"{user_id}|{movie_id}\n")

if __name__ == "__main__":
    app = Main()
    app.main()