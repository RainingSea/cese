from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from movie_manager import MovieManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        movies = movie_manager.search_movies(query)
        return render_template('search.html', movies=movies)
    return render_template('search.html')

@app.route('/recommendations', methods=['GET'])
def recommendations():
    preferences = {}  # Collect user preferences here
    recommendations = movie_manager.get_recommendations(preferences)
    return render_template('recommendations.html', recommendations=recommendations)

@app.route('/favorites', methods=['GET'])
def favorites():
    favorites = movie_manager.favorites
    return render_template('favorites.html', favorites=favorites)

if __name__ == '__main__':
    user_manager.load_users()
    movie_manager.load_movies()
    app.run(port=8351, debug=False)
