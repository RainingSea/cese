from flask import Flask, render_template, request, redirect, url_for, session
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_user_data()

    def load_user_data(self):
        if not os.path.exists('users.txt'):
            return {}
        with open('users.txt', 'r') as file:
            return {line.split('|')[0]: line.split('|')[1].strip() for line in file.readlines()}

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_user_data()
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def save_user_data(self) -> None:
        with open('users.txt', 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")

class DestinationRecommender:
    def __init__(self):
        self.destinations = self.load_destinations()

    def load_destinations(self) -> None:
        if not os.path.exists('destinations.txt'):
            self.destinations = []
            return
        with open('destinations.txt', 'r') as file:
            self.destinations = [line.strip() for line in file.readlines()]

    def get_recommendations(self, preferences: dict) -> list:
        # Simple recommendation logic based on preferences
        return [dest for dest in self.destinations if preferences['budget'] in dest]

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('preferences'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if request.method == 'POST':
        preferences = {
            'budget': request.form['budget'],
            'activities': request.form['activities'],
            'climate': request.form['climate']
        }
        session['preferences'] = preferences
        return redirect(url_for('recommendations'))
    return render_template('preferences.html')

@app.route('/recommendations')
def recommendations():
    preferences = session.get('preferences', {})
    recommendations = recommender.get_recommendations(preferences)
    return render_template('recommendations.html', recommendations=recommendations)

@app.route('/favorites')
def favorites():
    # Placeholder for favorites logic
    return render_template('favorites.html')

@app.route('/details/<destination>')
def details(destination):
    # Placeholder for details logic
    return render_template('details.html', destination=destination)

if __name__ == '__main__':
    user_manager = UserManager()
    recommender = DestinationRecommender()
    app.run(port=8444, debug=False)
