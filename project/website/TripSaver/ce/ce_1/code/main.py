import os
from flask import Flask, render_template, request, redirect, url_for, session
from html import escape

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

class UserManager:
    def __init__(self):
        self.users = []
        self.load_users()

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append((username, password))
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user[0] == username and user[1] == password for user in self.users)

    def save_users(self) -> None:
        with open('users.txt', 'w') as f:
            for user in self.users:
                f.write(f"{user[0]}|{user[1]}\n")

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                self.users = [line.strip().split('|') for line in f.readlines()]

class TripManager:
    def __init__(self):
        self.trips = []
        self.load_trips()

    def add_trip(self, start: str, destination: str, date: str) -> None:
        self.trips.append((start, destination, date))
        self.save_trips()

    def get_transportation_options(self, start: str, destination: str, date: str) -> list:
        # Dummy data for transportation options
        return [
            {"mode": "Bus", "cost": 10, "time": "1h 30m"},
            {"mode": "Train", "cost": 20, "time": "1h"},
            {"mode": "Car", "cost": 15, "time": "1h 15m"}
        ]

    def save_trips(self) -> None:
        with open('trips.txt', 'w') as f:
            for trip in self.trips:
                f.write(f"{trip[0]}|{trip[1]}|{trip[2]}\n")

    def load_trips(self) -> None:
        if os.path.exists('trips.txt'):
            with open('trips.txt', 'r') as f:
                self.trips = [line.strip().split('|') for line in f.readlines()]

user_manager = UserManager()
trip_manager = TripManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = escape(request.form['username'])
        password = escape(request.form['password'])
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Registration failed. Username already exists."
    return render_template('registration.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = escape(request.form['username'])
    password = escape(request.form['password'])
    if user_manager.login(username, password):
        session['username'] = username
        return redirect(url_for('trip_input'))
    return "Login failed. Please check your credentials."

@app.route('/trip_input', methods=['GET', 'POST'])
def trip_input():
    if request.method == 'POST':
        start = escape(request.form['start'])
        destination = escape(request.form['destination'])
        date = escape(request.form['date'])
        trip_manager.add_trip(start, destination, date)
        options = trip_manager.get_transportation_options(start, destination, date)
        return render_template('options_display.html', options=options)
    return render_template('trip_input.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8447, debug=False)
