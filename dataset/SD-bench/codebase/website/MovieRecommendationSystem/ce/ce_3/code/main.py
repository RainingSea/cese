from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from movie_manager import MovieManager
from favorites_manager import FavoritesManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager('users.txt')
movie_manager = MovieManager('movies.txt')
favorites_manager = FavoritesManager('favorites.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('main'))
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        return 'Username already exists'
    return render_template('register.html')

@app.route('/main')
def main():
    preferences = {'genres': ['Action', 'Comedy']}  # Example preferences
    recommendations = movie_manager.get_recommendations(preferences)
    return render_template('main.html', movies=recommendations)

@app.route('/movie/<title>')
def movie_detail(title):
    movie = movie_manager.get_movie_details(title)
    return render_template('movie_detail.html', movie=movie)

@app.route('/favorites')
def favorites():
    username = session.get('username')
    user_favorites = favorites_manager.get_favorites(username)
    return render_template('favorites.html', favorites=user_favorites)

if __name__ == '__main__':
    app.run(port=8649, debug=False)
