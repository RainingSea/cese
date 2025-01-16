from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from movie_manager import MovieManager
from favorites_manager import FavoritesManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
movie_manager = MovieManager('movies.txt')
favorites_manager = FavoritesManager('favorites.txt')

@app.route('/')
def login():
    """Renders the login page."""
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def do_login():
    """Handles user login."""
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/index')
def index():
    """Renders the index page with recommended movies."""
    recommended_movies = movie_manager.get_recommendations()
    return render_template('index.html', movies=recommended_movies)

@app.route('/favorites')
def favorites():
    """Renders the favorites page for the logged-in user."""
    if 'username' in session:
        user_favorites = favorites_manager.get_favorites(session['username'])
        return render_template('favorites.html', favorites=user_favorites)
    return redirect(url_for('login'))

@app.route('/add_favorite/<movie_title>')
def add_favorite(movie_title):
    """Adds a movie to the user's favorites."""
    if 'username' in session:
        favorites_manager.add_favorite(session['username'], movie_title)
    return redirect(url_for('index'))

@app.route('/remove_favorite/<movie_title>')
def remove_favorite(movie_title):
    """Removes a movie from the user's favorites."""
    if 'username' in session:
        favorites_manager.remove_favorite(session['username'], movie_title)
    return redirect(url_for('favorites'))

@app.route('/search', methods=['GET'])
def search():
    """Handles movie search functionality."""
    query = request.args.get('query', '')
    search_results = movie_manager.search_movies(query)
    return render_template('search_results.html', movies=search_results)

@app.route('/movie_detail/<title>')
def movie_detail(title):
    """Renders the details of a specific movie."""
    movie = user_manager.view_movie_details(title, movie_manager)
    if movie:
        return render_template('movie_detail.html', movie=movie)
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port=8651, debug=False)
