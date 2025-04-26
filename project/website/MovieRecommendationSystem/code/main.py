from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")

class MovieManager:
    def __init__(self):
        self.movies = {}
        self.load_movies()

    def load_movies(self) -> None:
        if os.path.exists('movies.txt'):
            with open('movies.txt', 'r') as file:
                for line in file:
                    movie_id, title, genre = line.strip().split('|')
                    self.movies[movie_id] = {'title': title, 'genre': genre}

    def get_recommendations(self, user_preferences: list) -> list:
        recommendations = []
        for movie_id, details in self.movies.items():
            if details['genre'] in user_preferences:
                recommendations.append({'id': movie_id, 'title': details['title'], 'genre': details['genre']})
        return recommendations[:5]  # Return first 5 recommendations

    def search_movies(self, query: str) -> list:
        return [details for details in self.movies.values() if query.lower() in details['title'].lower()]

    def get_movie_details(self, movie_id: str) -> dict:
        return self.movies.get(movie_id, {})

    def load_favorites(self, username: str) -> list:
        favorites = []
        if os.path.exists('favorites.txt'):
            with open('favorites.txt', 'r') as file:
                for line in file:
                    user, movie_id = line.strip().split('|')
                    if user == username:
                        favorites.append(movie_id)
        return favorites

    def add_to_favorites(self, username: str, movie_id: str) -> None:
        if not self.is_favorite(username, movie_id):
            with open('favorites.txt', 'a') as file:
                file.write(f"{username}|{movie_id}\n")

    def remove_from_favorites(self, username: str, movie_id: str) -> None:
        lines = []
        if os.path.exists('favorites.txt'):
            with open('favorites.txt', 'r') as file:
                lines = file.readlines()
        with open('favorites.txt', 'w') as file:
            for line in lines:
                if line.strip() != f"{username}|{movie_id}":
                    file.write(line)

    def is_favorite(self, username: str, movie_id: str) -> bool:
        favorites = self.load_favorites(username)
        return movie_id in favorites

user_manager = UserManager()
movie_manager = MovieManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('recommendations'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/recommendations')
def recommendations():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_preferences = ['Action', 'Comedy']  # Example preferences
    recommendations = movie_manager.get_recommendations(user_preferences)
    return render_template('recommendations.html', recommendations=recommendations)

@app.route('/movie/<movie_id>')
def movie_detail(movie_id):
    movie_details = movie_manager.get_movie_details(movie_id)
    return render_template('movie_detail.html', movie=movie_details)

@app.route('/favorites')
def favorites():
    if 'username' not in session:
        return redirect(url_for('login'))
    favorites = movie_manager.load_favorites(session['username'])
    favorite_movies = [movie_manager.get_movie_details(movie_id) for movie_id in favorites]
    return render_template('favorites.html', favorites=favorite_movies)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    search_results = movie_manager.search_movies(query)
    return render_template('search_results.html', results=search_results)

@app.route('/add_favorite/<movie_id>', methods=['POST'])
def add_favorite(movie_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    movie_manager.add_to_favorites(session['username'], movie_id)
    return redirect(url_for('favorites'))

@app.route('/remove_favorite/<movie_id>', methods=['POST'])
def remove_favorite(movie_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    movie_manager.remove_from_favorites(session['username'], movie_id)
    return redirect(url_for('favorites'))

if __name__ == '__main__':
    app.run(port=8189, debug=False)
