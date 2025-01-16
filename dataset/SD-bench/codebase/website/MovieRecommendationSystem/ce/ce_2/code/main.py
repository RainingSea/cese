from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from movie import Movie
from favorites import Favorites
from movie_recommendation import MovieRecommendation

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users[username] = password
    return users

def load_movies():
    movies = {}
    with open('movies.txt', 'r') as file:
        for line in file:
            title, description, rating = line.strip().split('|')
            movies[title] = Movie(title, description, float(rating))
    return movies

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    movies = load_movies()
    recommendations = MovieRecommendation(user_preferences={}).recommend_movies()
    return render_template('home.html', movies=recommendations)

@app.route('/movie/<title>')
def movie_detail(title):
    movies = load_movies()
    movie = movies.get(title)
    return render_template('movie_detail.html', movie=movie)

@app.route('/favorites')
def favorites():
    username = session.get('username')
    favorites = Favorites(username)
    favorite_movies = favorites.get_favorites()
    return render_template('favorites.html', favorites=favorite_movies)

if __name__ == '__main__':
    app.run(port=8648, debug=False)
