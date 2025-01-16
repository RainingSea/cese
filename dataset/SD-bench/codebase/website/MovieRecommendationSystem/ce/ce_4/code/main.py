from flask import Flask, render_template, request, redirect, url_for
from user_manager import UserManager
from movie_manager import MovieManager
from favorites_manager import FavoritesManager

app = Flask(__name__)

user_manager = UserManager('users.txt')
movie_manager = MovieManager('movies.txt')
favorites_manager = FavoritesManager('favorites.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home', methods=['POST'])
def home():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        recommendations = movie_manager.get_recommendations({})
        return render_template('index.html', recommendations=recommendations)
    return redirect(url_for('login'))

@app.route('/movie/<movie_id>')
def movie_detail(movie_id):
    movie_details = movie_manager.get_movie_details(movie_id)
    return render_template('movie_detail.html', movie=movie_details)

@app.route('/favorites')
def favorites():
    # Assuming a logged-in user with username 'current_user'
    current_user = 'current_user'  # Placeholder for actual user session management
    user_favorites = favorites_manager.get_favorites(current_user)
    return render_template('favorites.html', favorites=user_favorites)

if __name__ == '__main__':
    app.run(port=8650, debug=False)
