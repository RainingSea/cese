from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

class UserManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file
        if not os.path.exists(self.users_file):
            open(self.users_file, 'w').close()

    def register(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                if line.startswith(username + '|'):
                    return False
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == username and parts[1] == password:
                    return True
        return False

class MovieManager:
    def __init__(self, movies_file='movies.txt'):
        self.movies_file = movies_file
        if not os.path.exists(self.movies_file):
            open(self.movies_file, 'w').close()
        self.movies = self.load_movies()

    def load_movies(self):
        movies = []
        with open(self.movies_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 5:
                    movies.append({
                        'id': parts[0],
                        'title': parts[1],
                        'description': parts[2],
                        'rating': parts[3],
                        'genres': parts[4].split(',')
                    })
        return movies

    def get_recommendations(self, username=None):
        return self.movies[:5]  # Simple: return first 5 movies as recommendations

    def search(self, query):
        return [movie for movie in self.movies if query.lower() in movie['title'].lower()]

    def get_details(self, movie_id):
        for movie in self.movies:
            if movie['id'] == movie_id:
                return movie
        return None

class FavoritesManager:
    def __init__(self, favorites_file='favorites.txt'):
        self.favorites_file = favorites_file
        if not os.path.exists(self.favorites_file):
            open(self.favorites_file, 'w').close()

    def add_favorite(self, username, movie_id):
        with open(self.favorites_file, 'a') as f:
            f.write(f"{username}|{movie_id}\n")
        return True

    def remove_favorite(self, username, movie_id):
        lines = []
        removed = False
        with open(self.favorites_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] != username or parts[1] != movie_id:
                    lines.append(line)
                else:
                    removed = True
        with open(self.favorites_file, 'w') as f:
            f.writelines(lines)
        return removed

    def get_favorites(self, username):
        favorites = []
        with open(self.favorites_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == username:
                    favorites.append(parts[1])
        return favorites

user_manager = UserManager()
movie_manager = MovieManager()
favorites_manager = FavoritesManager()

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    recommendations = movie_manager.get_recommendations(session['username'])
    return render_template('index.html', recommendations=recommendations, current_user=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        query = request.form['query']
        results = movie_manager.search(query)
        return render_template('search.html', results=results, current_user=session['username'])
    return render_template('search.html', results=None, current_user=session['username'])

@app.route('/details/<movie_id>')
def details(movie_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    movie = movie_manager.get_details(movie_id)
    if not movie:
        return redirect(url_for('index'))
    favorites = favorites_manager.get_favorites(session['username'])
    is_favorite = movie_id in favorites
    return render_template('details.html', movie=movie, is_favorite=is_favorite, current_user=session['username'])

@app.route('/favorites')
def favorites():
    if 'username' not in session:
        return redirect(url_for('login'))
    favorite_ids = favorites_manager.get_favorites(session['username'])
    favorites = [movie_manager.get_details(mid) for mid in favorite_ids]
    favorites = [f for f in favorites if f is not None]
    return render_template('favorites.html', favorites=favorites, current_user=session['username'])

@app.route('/add_favorite/<movie_id>')
def add_favorite(movie_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    favorites_manager.add_favorite(session['username'], movie_id)
    return redirect(url_for('details', movie_id=movie_id))

@app.route('/remove_favorite/<movie_id>')
def remove_favorite(movie_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    favorites_manager.remove_favorite(session['username'], movie_id)
    return redirect(url_for('favorites'))

if __name__ == '__main__':
    app.run(port=8003, debug=False)
