from flask import Flask, render_template, request, redirect, session, url_for, escape
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def register(self, username: str, password: str) -> str:
        if any(user[0] == username for user in self.users):
            return "Username already exists"  # Username already exists
        self.users.append([username, password])
        self.save_users()
        return "Registration successful"

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')

    def login(self, username: str, password: str) -> str:
        if any(user[0] == username and user[1] == password for user in self.users):
            session['username'] = username
            return "Login successful"
        return "Invalid credentials"

    def logout(self):
        session.pop('username', None)

    def is_logged_in(self) -> bool:
        return 'username' in session

class TripManager:
    def __init__(self):
        self.trips = self.load_trips()

    def load_trips(self):
        if not os.path.exists('trips.txt'):
            return []
        with open('trips.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def add_trip(self, start: str, destination: str, date: str):
        self.trips.append([start, destination, date])
        self.save_trips()

    def save_trips(self):
        with open('trips.txt', 'w') as file:
            for trip in self.trips:
                file.write('|'.join(trip) + '\n')

    def get_suggestions(self, start: str, destination: str, date: str):
        return [{"mode": "Bus", "cost": 10, "time": "1 hour"}, {"mode": "Train", "cost": 20, "time": "30 minutes"}]

    def save_preference(self, user: str, trip: str):
        pass

user_manager = UserManager()
trip_manager = TripManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = escape(request.form['username'])
        password = escape(request.form['password'])
        login_message = user_manager.login(username, password)
        if login_message == "Login successful":
            return redirect(url_for('trip_input'))
        else:
            return render_template('login.html', error=login_message)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = escape(request.form['username'])
        password = escape(request.form['password'])
        registration_message = user_manager.register(username, password)
        if registration_message == "Registration successful":
            return redirect(url_for('login'))
        else:
            return render_template('registration.html', error=registration_message)
    return render_template('registration.html')

@app.route('/trip_input', methods=['GET', 'POST'])
def trip_input():
    if not user_manager.is_logged_in():
        return redirect(url_for('login'))
    if request.method == 'POST':
        start = request.form['start']
        destination = request.form['destination']
        date = request.form['date']
        trip_manager.add_trip(start, destination, date)
        return redirect(url_for('results', start=start, destination=destination, date=date))
    return render_template('trip_input.html')

@app.route('/results')
def results():
    if not user_manager.is_logged_in():
        return redirect(url_for('login'))
    start = request.args.get('start')
    destination = request.args.get('destination')
    date = request.args.get('date')
    suggestions = trip_manager.get_suggestions(start, destination, date)
    return render_template('results.html', suggestions=suggestions)

@app.route('/logout')
def logout():
    user_manager.logout()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8449, debug=False)
