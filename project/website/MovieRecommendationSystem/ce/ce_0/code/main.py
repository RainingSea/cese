from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class Movie:
    def __init__(self, title, description, rating):
        self.title = title
        self.description = description
        self.rating = float(rating)

    def get_details(self):
        return {
            'title': self.title,
            'description': self.description,
            'rating': self.rating
        }

class FileHandler:
    def __init__(self):
        self.users_file = 'users.txt'
        self.movies_file = 'movies.txt'
        self.favorites_file = 'favorites.txt'

    def read_users(self):
        users = {}
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users[username] = password
        except FileNotFoundError:
            pass
        return users

    def write_user(self, username, password):
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def read_movies(self):
        movies = []
        try:
            with open(self.movies_file, 'r') as f:
                for line in f:
                    title, description, rating = line.strip().split('|')
                    movies.append(Movie(title, description, rating))
        except FileNotFoundError:
            pass
        return movies

    def read_favorites(self, username):
        favorites = []
        try:
            with open(self.favorites_file, 'r') as f:
                for line in f:
                    user, title = line.strip().split('|')
                    if user == username:
                        favorites.append(title)
        except FileNotFoundError:
            pass
        return favorites

    def write_favorite(self, username, title):
        with open(self.favorites_file, 'a') as f:
            f.write(f"{username}|{title}\n")
        return True

    def remove_favorite(self, username, title):
        favorites = []
        removed = False
        try:
            with open(self.favorites_file, 'r') as f:
                favorites = f.readlines()
            
            with open(self.favorites_file, 'w') as f:
                for line in favorites:
                    user, fav_title = line.strip().split('|')
                    if not (user == username and fav_title == title):
                        f.write(line)
                    else:
                        removed = True
        except FileNotFoundError:
            pass
        return removed

class MovieApp:
    def __init__(self):
        self.current_user = None
        self.file_handler = FileHandler()

    def login(self, username, password):
        users = self.file_handler.read_users()
        if username in users and users[username] == password:
            self.current_user = username
            return True
        return False

    def register(self, username, password):
        users = self.file_handler.read_users()
        if username in users:
            return False
        self.file_handler.write_user(username, password)
        self.current_user = username
        return True

    def get_recommendations(self):
        movies = self.file_handler.read_movies()
        return sorted(movies, key=lambda x: x.rating, reverse=True)[:5]

    def search_movies(self, query):
        movies = self.file_handler.read_movies()
        return [movie for movie in movies if query.lower() in movie.title.lower()]

    def get_movie_details(self, title):
        movies = self.file_handler.read_movies()
        for movie in movies:
            if movie.title == title:
                return movie
        return None

    def add_favorite(self, title):
        if self.current_user:
            return self.file_handler.write_favorite(self.current_user, title)
        return False

    def remove_favorite(self, title):
        if self.current_user:
            return self.file_handler.remove_favorite(self.current_user, title)
        return False

    def get_favorites(self):
        if not self.current_user:
            return []
        favorites = self.file_handler.read_favorites(self.current_user)
        movies = self.file_handler.read_movies()
        return [movie for movie in movies if movie.title in favorites]

movie_app = MovieApp()

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    recommendations = movie_app.get_recommendations()
    return render_template('dashboard.html', recommendations=recommendations)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if movie_app.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if movie_app.register(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        return render_template('login.html', error='Username already exists')
    return render_template('login.html', register=True)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' not in session:
        return redirect(url_for('login'))
    results = []
    if request.method == 'POST':
        query = request.form['query']
        results = movie_app.search_movies(query)
    return render_template('search.html', results=results)

@app.route('/movie/<title>')
def movie_details(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    movie = movie_app.get_movie_details(title)
    if not movie:
        return redirect(url_for('home'))
    return render_template('movie_details.html', movie=movie)

@app.route('/favorites')
def favorites():
    if 'username' not in session:
        return redirect(url_for('login'))
    favorites = movie_app.get_favorites()
    return render_template('favorites.html', favorites=favorites)

@app.route('/add_favorite/<title>')
def add_favorite(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    movie_app.add_favorite(title)
    return redirect(url_for('movie_details', title=title))

@app.route('/remove_favorite/<title>')
def remove_favorite(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    movie_app.remove_favorite(title)
    return redirect(url_for('favorites'))

if __name__ == '__main__':
    app.run(port=8002, debug=False)
