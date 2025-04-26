from flask import Flask, render_template, request, redirect, url_for, session
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def load_users(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def save_users(self):
        with open('users.txt', 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")

    def add_user(self, username: str, password: str):
        self.users[username] = password
        self.save_users()

    def validate_user(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class MovieManager:
    def __init__(self):
        self.movies = {}
        self.load_movies()

    def load_movies(self):
        if os.path.exists('movies.txt'):
            with open('movies.txt', 'r') as file:
                for line in file:
                    movie_id, title, description, rating = line.strip().split('|')
                    self.movies[movie_id] = {
                        'title': title,
                        'description': description,
                        'rating': rating
                    }

    def save_movies(self):
        with open('movies.txt', 'w') as file:
            for movie_id, details in self.movies.items():
                file.write(f"{movie_id}|{details['title']}|{details['description']}|{details['rating']}\n")

    def get_movie_details(self, movie_id: str) -> dict:
        return self.movies.get(movie_id, {})

    def get_recommendations(self, preferences: list) -> list:
        # Placeholder for recommendations logic
        return list(self.movies.values())[:5]

user_manager = UserManager()
movie_manager = MovieManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.validate_user(username, password):
            session['username'] = username
            return redirect(url_for('recommendations'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.add_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/recommendations')
def recommendations():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('recommendations.html', movies=movie_manager.get_recommendations([]))

@app.route('/search', methods=['GET', 'POST'])
def search_movies():
    if request.method == 'POST':
        query = request.form['query']
        # Placeholder for search logic
        return render_template('search_results.html', movies=movie_manager.movies)
    return render_template('search_results.html', movies=[])

@app.route('/favorites')
def favorites():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('favorites.html')

if __name__ == '__main__':
    app.run(port=8187, debug=False)
