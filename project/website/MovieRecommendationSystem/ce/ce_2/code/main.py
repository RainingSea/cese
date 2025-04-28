from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from MovieManager import MovieManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'

user_manager = UserManager()
movie_manager = MovieManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('search'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Registration failed"
    return render_template('register.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        movies = movie_manager.search_movies(query)
        return render_template('search.html', movies=movies)
    return render_template('search.html')

@app.route('/movie/<title>')
def movie_detail(title):
    movie = movie_manager.get_movie_details(title)
    return render_template('movie_detail.html', movie=movie)

@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    username = session.get('username')
    if request.method == 'POST':
        action = request.form['action']
        movie_title = request.form['movie_title']
        if action == 'add':
            movie_manager.add_to_favorites(username, movie_title)
        elif action == 'remove':
            movie_manager.remove_from_favorites(username, movie_title)
    favorites = movie_manager.favorites.get(username, [])
    return render_template('favorites.html', favorites=favorites)

if __name__ == '__main__':
    user_manager.load_users()
    movie_manager.load_movies()
    movie_manager.load_favorites()
    app.run(port=8352, debug=False)
