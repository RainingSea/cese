from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

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

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                self.users = [line.strip().split('|') for line in file.readlines()]

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')

class TripManager:
    def __init__(self):
        self.trips = []
        self.load_trips()

    def add_trip(self, start: str, destination: str, date: str) -> None:
        self.trips.append((start, destination, date))
        self.save_trips()

    def get_transport_options(self, start: str, destination: str, date: str) -> list:
        # Dummy transport options for demonstration
        return [
            {"mode": "Bus", "cost": 20, "time": "2 hours"},
            {"mode": "Train", "cost": 35, "time": "1.5 hours"},
            {"mode": "Car", "cost": 50, "time": "1 hour"},
        ]

    def load_trips(self) -> None:
        if os.path.exists('trips.txt'):
            with open('trips.txt', 'r') as file:
                self.trips = [line.strip().split('|') for line in file.readlines()]

    def save_trips(self) -> None:
        with open('trips.txt', 'w') as file:
            for trip in self.trips:
                file.write('|'.join(trip) + '\n')

user_manager = UserManager()
trip_manager = TripManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect(url_for('trip_details'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists.')
    return render_template('register.html')

@app.route('/trip_details', methods=['GET', 'POST'])
def trip_details():
    if request.method == 'POST':
        start = request.form['start']
        destination = request.form['destination']
        date = request.form['date']
        trip_manager.add_trip(start, destination, date)
        options = trip_manager.get_transport_options(start, destination, date)
        return render_template('results.html', options=options)
    return render_template('trip_details.html')

if __name__ == '__main__':
    app.run(port=8276, debug=False)
