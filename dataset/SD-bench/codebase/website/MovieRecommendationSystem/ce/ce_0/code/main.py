from flask import Flask, render_template, request, redirect, url_for
from UserManager import UserManager
from MovieManager import MovieManager
from FavoritesManager import FavoritesManager

app = Flask(__name__)

user_manager = UserManager()
movie_manager = MovieManager()
favorites_manager = FavoritesManager()

@app.route('/')
def home():
    return render_template('home.html', movies=movie_manager.movies)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == '__main__':
    app.run(port=8646, debug=False)
