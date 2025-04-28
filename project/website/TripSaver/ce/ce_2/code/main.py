from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                return [line.strip().split('|') for line in file.readlines()]
        return []

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append([username, password])
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                session['username'] = username
                return True
        return False

    def logout(self):
        session.pop('username', None)

class TripManager:
    def __init__(self):
        self.trips = self.load_trips()

    def load_trips(self):
        if os.path.exists('trips.txt'):
            with open('trips.txt', 'r') as file:
                return [line.strip().split('|') for line in file.readlines()]
        return []

    def add_trip(self, start: str, destination: str, date: str):
        self.trips.append([start, destination, date])
        self.save_trips()

    def save_trips(self):
        with open('trips.txt', 'w') as file:
            for trip in self.trips:
                file.write('|'.join(trip) + '\n')

    def get_suggestions(self, start: str, destination: str, date: str):
        # Placeholder for transportation suggestions logic
        return [{"option": "Bus", "cost": 10, "time": "30 mins"}, 
                {"option": "Train", "cost": 15, "time": "20 mins"}]

    def save_option(self, option: str):
        with open('saved_options.txt', 'a') as file:
            file.write(option + '\n')

user_manager = UserManager()
trip_manager = TripManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect('/trip_input')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
    return render_template('registration.html')

@app.route('/trip_input', methods=['GET', 'POST'])
def trip_input():
    if request.method == 'POST':
        start = request.form['start']
        destination = request.form['destination']
        date = request.form['date']
        trip_manager.add_trip(start, destination, date)
        suggestions = trip_manager.get_suggestions(start, destination, date)
        return render_template('suggestions.html', suggestions=suggestions)
    return render_template('trip_input.html')

@app.route('/logout')
def logout():
    user_manager.logout()
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8448, debug=False)
