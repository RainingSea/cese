from flask import Flask, render_template, request, redirect, url_for, session
import json
from data_manager import DataManager
from models import User, Preferences, Destination, RecommendationEngine, Favorites

app = Flask(__name__)
app.secret_key = 'your_secret_key'
data_manager = DataManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = data_manager.load_users()
        if username and password:
            if username in [user['username'] for user in users]:
                return render_template('register.html', error="Username already taken.")
            user = User(username, password)
            users.append(user.to_dict())
            data_manager.save_users(users)
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = data_manager.load_users()
    if any(user['username'] == username and user['password'] == password for user in users):
        session['username'] = username
        return redirect(url_for('preferences'))
    return render_template('login.html', error="Invalid credentials.")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if request.method == 'POST':
        try:
            budget = float(request.form['budget'])
            activities = request.form.getlist('activities')
            climate = request.form['climate']
            if budget < 0 or not activities or not climate:
                raise ValueError("Invalid input values.")
            preferences = Preferences(budget, activities, climate)
            data_manager.save_preferences(preferences.to_dict())
            return redirect(url_for('recommendations'))
        except (ValueError, TypeError):
            return render_template('preferences.html', error="Please provide valid inputs.")
    return render_template('preferences.html')

@app.route('/recommendations')
def recommendations():
    preferences_data = data_manager.load_preferences()
    preferences = Preferences(**preferences_data)
    destinations = data_manager.load_destinations()
    recommendation_engine = RecommendationEngine(destinations)
    recommendations = recommendation_engine.generate_recommendations(preferences)
    return render_template('recommendations.html', recommendations=recommendations)

@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    user = session.get('username')
    if request.method == 'POST':
        destination_name = request.form['destination_name']
        if destination_name:
            favorites = Favorites(user)
            favorites.add_favorite(Destination(destination_name, [], '', 0))
            data_manager.save_favorites(user, favorites.get_favorites())
    user_favorites = data_manager.load_favorites(user)
    return render_template('favorites.html', favorites=user_favorites)

@app.route('/details/<destination_name>')
def details(destination_name):
    destinations = data_manager.load_destinations()
    destination_details = next((dest for dest in destinations if dest['name'] == destination_name), None)
    return render_template('details.html', details=destination_details)

if __name__ == '__main__':
    app.run(port=8676, debug=False)
