from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

class UserManager:
    def __init__(self):
        self.users = []
        self.load_user_data()

    def register(self, username: str, password: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        self.users.append({'username': username, 'password': password})
        self.save_user_data()
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                return True
        return False

    def save_user_data(self) -> None:
        with open('users.txt', 'w') as f:
            for user in self.users:
                f.write(f"{user['username']}|{user['password']}\n")

    def load_user_data(self) -> None:
        try:
            with open('users.txt', 'r') as f:
                self.users = []
                for line in f:
                    username, password = line.strip().split('|')
                    self.users.append({'username': username, 'password': password})
        except FileNotFoundError:
            self.users = []

class RecommendationEngine:
    def __init__(self):
        self.preferences = []
        self.destinations = []
        self.load_destinations()

    def generate_recommendations(self, user_preferences: dict) -> list:
        recommendations = []
        for destination in self.destinations:
            if (destination['budget'] <= user_preferences['budget'] and
                destination['climate'] == user_preferences['climate'] and
                any(activity in destination['activities'] for activity in user_preferences['activities'])):
                recommendations.append(destination)
        return recommendations

    def load_destinations(self) -> None:
        try:
            with open('destinations.txt', 'r') as f:
                self.destinations = []
                for line in f:
                    name, budget, climate, activities = line.strip().split('|')
                    self.destinations.append({
                        'name': name,
                        'budget': int(budget),
                        'climate': climate,
                        'activities': activities.split(',')
                    })
        except FileNotFoundError:
            self.destinations = []

    def save_destinations(self) -> None:
        with open('destinations.txt', 'w') as f:
            for destination in self.destinations:
                activities = ','.join(destination['activities'])
                f.write(f"{destination['name']}|{destination['budget']}|{destination['climate']}|{activities}\n")

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if user_manager.register(username, password):
        return redirect('/')
    return "Registration failed. Username may already exist."

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        return redirect('/preferences')
    return "Login failed. Check your credentials."

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if request.method == 'POST':
        user_preferences = {
            'budget': int(request.form['budget']),
            'activities': request.form.getlist('activities'),
            'climate': request.form['climate']
        }
        recommendations = recommendation_engine.generate_recommendations(user_preferences)
        return render_template('recommendations.html', recommendations=recommendations)
    return render_template('preferences.html')

user_manager = UserManager()
recommendation_engine = RecommendationEngine()

if __name__ == '__main__':
    app.run(port=8272, debug=False)
