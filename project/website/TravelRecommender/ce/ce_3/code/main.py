from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from preferences import Preferences
from favorites import Favorites
from recommendation_engine import RecommendationEngine

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and preferences
def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users[username] = password
    return users

def load_preferences():
    preferences = {}
    with open('preferences.txt', 'r') as file:
        for line in file:
            username, budget, activities, climate = line.strip().split('|')
            preferences[username] = Preferences(budget, activities.split(','), climate)
    return preferences

def load_favorites():
    favorites = {}
    with open('favorites.txt', 'r') as file:
        for line in file:
            username, favorite_destinations = line.strip().split('|')
            favorites[username] = Favorites(username)
            for destination in favorite_destinations.split(','):
                favorites[username].save_favorite(destination)
    return favorites

users = load_users()
preferences = load_preferences()
favorites = load_favorites()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            users[username] = password
            with open('users.txt', 'a') as file:
                file.write(f"{username}|{password}\n")
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if users.get(username) == password:
        session['username'] = username
        return redirect(url_for('preferences_page'))
    return redirect(url_for('login'))

@app.route('/preferences', methods=['GET', 'POST'])
def preferences_page():
    if request.method == 'POST':
        budget = request.form['budget']
        activities = request.form.getlist('activities')
        climate = request.form['climate']
        user_preferences = Preferences(budget, activities, climate)
        preferences[session['username']] = user_preferences
        with open('preferences.txt', 'a') as file:
            file.write(f"{session['username']}|{budget}|{','.join(activities)}|{climate}\n")
        return redirect(url_for('recommendations'))
    return render_template('preferences.html')

@app.route('/recommendations')
def recommendations():
    user_preferences = preferences.get(session['username'])
    if user_preferences:
        recommender = RecommendationEngine([])
        recommendations = recommender.generate_recommendations(user_preferences.__dict__)
        return render_template('recommendations.html', recommendations=recommendations)
    return redirect(url_for('preferences_page'))

@app.route('/favorites')
def favorites_page():
    user_favorites = favorites.get(session['username'])
    return render_template('favorites.html', favorites=user_favorites.load_favorites())

@app.route('/details/<destination_name>')
def details(destination_name):
    recommender = RecommendationEngine([])
    details = recommender.get_destination_details(destination_name)
    return render_template('details.html', details=details)

if __name__ == '__main__':
    app.run(port=8674, debug=False)
