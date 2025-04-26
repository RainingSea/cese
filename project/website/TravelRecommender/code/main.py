from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class Main:
    def __init__(self):
        self.user_manager = UserManager('users.txt')
        self.recommendation_engine = RecommendationEngine('preferences.txt', 'destinations.txt')

    def main(self):
        app.run(port=8273, debug=False)

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.users = self.load_users()

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_user_data()
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def load_users(self) -> dict:
        users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users[username] = password
        return users

    def save_user_data(self) -> None:
        with open(self.users_file, 'w') as f:
            for username, password in self.users.items():
                f.write(f"{username}|{password}\n")

class RecommendationEngine:
    def __init__(self, preferences_file: str, destinations_file: str):
        self.preferences_file = preferences_file
        self.destinations_file = destinations_file
        self.destinations = self.load_destinations()

    def generate_recommendations(self, preferences: dict) -> list:
        recommendations = []
        for destination, details in self.destinations.items():
            if self.match_preferences(details, preferences):
                recommendations.append(destination)
        return recommendations

    def load_destinations(self) -> dict:
        destinations = {}
        if os.path.exists(self.destinations_file):
            with open(self.destinations_file, 'r') as f:
                for line in f:
                    name, activities, climate, cost = line.strip().split('|')
                    destinations[name] = {
                        'activities': activities.split(','),
                        'climate': climate,
                        'cost': int(cost)
                    }
        return destinations

    def match_preferences(self, details: dict, preferences: dict) -> bool:
        return (details['cost'] <= preferences['budget'] and
                details['climate'] == preferences['climate'] and
                any(activity in preferences['activities'] for activity in details['activities']))

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('registration.html')
    username = request.form['username']
    password = request.form['password']
    if main.user_manager.register(username, password):
        return redirect(url_for('login'))
    return render_template('registration.html', error="Username already taken.")

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if main.user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('preferences'))
    return render_template('login.html', error="Invalid credentials.")

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if request.method == 'POST':
        preferences = {
            'budget': int(request.form['budget']),
            'activities': request.form.getlist('activities'),
            'climate': request.form['climate']
        }
        recommendations = main.recommendation_engine.generate_recommendations(preferences)
        return render_template('recommendations.html', recommendations=recommendations)
    return render_template('preferences.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/favorites', methods=['POST'])
def save_favorite():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    destination = request.form['destination']
    favorites = session.get('favorites', [])
    if destination not in favorites:
        favorites.append(destination)
        session['favorites'] = favorites
    return redirect(url_for('preferences'))

@app.before_request
def before_request():
    if request.endpoint not in ['login', 'register'] and not any_route_that_requires_authentication():
        return redirect(url_for('login'))

def any_route_that_requires_authentication():
    return 'username' in session

if __name__ == '__main__':
    main = Main()
    main.main()