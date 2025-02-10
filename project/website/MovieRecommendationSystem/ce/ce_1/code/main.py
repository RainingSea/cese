from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from MovieManager import MovieManager

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
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/index')
def index():
    recommendations = movie_manager.get_recommendations(session.get('username', ''))
    return render_template('index.html', recommendations=recommendations)

@app.route('/movie/<movie_id>')
def movie_detail(movie_id):
    movie = movie_manager.get_movie_details(movie_id)
    return render_template('movie_detail.html', movie=movie)

@app.route('/favorites')
def favorites():
    user_favorites = movie_manager.load_favorites(session.get('username', ''))
    return render_template('favorites.html', favorites=user_favorites)

if __name__ == '__main__':
    app.run(port=8647, debug=False)
