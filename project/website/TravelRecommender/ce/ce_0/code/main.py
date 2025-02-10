from flask import Flask, request, render_template, redirect, url_for
from typing import List
import os

app = Flask(__name__)

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class Preferences:
    def __init__(self, budget: float, activities: List[str], climate: str):
        self.budget = budget
        self.activities = activities
        self.climate = climate

class Destination:
    def __init__(self, name: str, activities: List[str], climate: str, cost: float):
        self.name = name
        self.activities = activities
        self.climate = climate
        self.cost = cost

def load_users() -> List[User]:
    users = []
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    return users

def load_preferences() -> List[Preferences]:
    preferences = []
    if os.path.exists('preferences.txt'):
        with open('preferences.txt', 'r') as file:
            for line in file:
                username, budget, activities, climate = line.strip().split('|')
                activities_list = activities.split(',')
                preferences.append(Preferences(float(budget), activities_list, climate))
    return preferences

def load_destinations() -> List[Destination]:
    destinations = []
    if os.path.exists('destinations.txt'):
        with open('destinations.txt', 'r') as file:
            for line in file:
                name, activities, climate, cost = line.strip().split('|')
                activities_list = activities.split(',')
                destinations.append(Destination(name, activities_list, climate, float(cost)))
    return destinations

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password:
            with open('users.txt', 'a') as file:
                file.write(f"{username}|{password}\n")
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    if request.method == 'POST':
        username = request.form['username']
        budget = float(request.form['budget'])
        activities = request.form['activities'].split(',')
        climate = request.form['climate']
        preferences = Preferences(budget, activities, climate)
        with open('preferences.txt', 'a') as file:
            file.write(f"{username}|{preferences.budget}|{','.join(preferences.activities)}|{preferences.climate}\n")
        
        # Generate recommendations based on preferences
        destinations = load_destinations()
        recommended_destinations = [d for d in destinations if d.cost <= budget and d.climate == climate]
        return render_template('recommendations.html', recommendations=recommended_destinations)
    
    return render_template('recommendations.html')

if __name__ == '__main__':
    app.run(port=8671, debug=False)
