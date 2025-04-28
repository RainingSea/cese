from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append({'username': username, 'password': password})
        except FileNotFoundError:
            pass
        return users

    def register(self, username: str, password: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        self.users.append({'username': username, 'password': password})
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                return True
        return False

class PreferenceManager:
    def __init__(self):
        self.preferences = self.load_preferences()

    def load_preferences(self):
        preferences = {}
        try:
            with open('preferences.txt', 'r') as file:
                for line in file:
                    username, pref = line.strip().split('|')
                    preferences[username] = pref
        except FileNotFoundError:
            pass
        return preferences

    def save_preferences(self, username: str, preferences: dict) -> None:
        self.preferences[username] = preferences
        with open('preferences.txt', 'a') as file:
            file.write(f"{username}|{preferences}\n")

class RecommendationEngine:
    def __init__(self):
        self.destinations = self.load_destinations()

    def load_destinations(self):
        destinations = []
        try:
            with open('destinations.txt', 'r') as file:
                for line in file:
                    destinations.append(line.strip())
        except FileNotFoundError:
            pass
        return destinations

    def generate_recommendations(self, preferences: dict) -> list:
        # Placeholder for actual recommendation logic
        return self.destinations[:5]  # Return first 5 destinations as a simple example

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if UserManager().register(username, password):
            return redirect(url_for('login'))
        else:
            return "Username already exists!"
    return render_template('registration.html')

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if request.method == 'POST':
        username = session.get('username')
        preferences = request.form.to_dict()
        PreferenceManager().save_preferences(username, preferences)
        return redirect(url_for('recommendations'))
    return render_template('preferences.html')

@app.route('/recommendations')
def recommendations():
    username = session.get('username')
    preferences = PreferenceManager().preferences.get(username, {})
    recommendations = RecommendationEngine().generate_recommendations(preferences)
    return render_template('recommendations.html', recommendations=recommendations)

@app.route('/favorites')
def favorites():
    # Placeholder for favorites logic
    return render_template('favorites.html')

if __name__ == '__main__':
    app.run(port=8443, debug=False)
