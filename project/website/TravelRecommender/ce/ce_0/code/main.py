from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = {}
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users[username] = password
        return users

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class RecommendationEngine:
    def __init__(self):
        self.destinations = self.load_destinations()

    def load_destinations(self):
        # Placeholder for loading destinations from a file or database
        return ["Paris", "New York", "Tokyo", "Sydney"]

    def generate_recommendations(self, preferences: dict) -> list:
        # Simple recommendation logic based on preferences
        return self.destinations[:3]  # Return first three destinations for demo

    def get_destination_details(self, destination: str) -> dict:
        # Placeholder for detailed information about a destination
        return {"name": destination, "description": f"Details about {destination}"}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Username already exists!"
    return render_template('register.html')

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if request.method == 'POST':
        budget = request.form['budget']
        activities = request.form['activities']
        climate = request.form['climate']
        preferences = {'budget': budget, 'activities': activities, 'climate': climate}
        recommendations = recommendation_engine.generate_recommendations(preferences)
        return render_template('recommendations.html', recommendations=recommendations)
    return render_template('preferences.html')

user_manager = UserManager()
recommendation_engine = RecommendationEngine()

if __name__ == '__main__':
    app.run(port=8442, debug=False)
