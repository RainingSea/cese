import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.trip_manager = TripManager()

    def main(self):
        self.user_manager.load_users()
        self.trip_manager.load_trips()
        app.run(port=8446, debug=False)

class UserManager:
    def __init__(self):
        self.users = {}

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def load_users(self) -> None:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for username, password in self.users.items():
                file.write(f"{username}|{password}\n")

class TripManager:
    def __init__(self):
        self.trips = []

    def add_trip(self, start: str, destination: str, date: str) -> None:
        self.trips.append({'start': start, 'destination': destination, 'date': date})
        self.save_trip_options()

    def get_transportation_options(self, start: str, destination: str, date: str) -> list:
        # Simulated transportation options for demo purposes
        return [
            {'mode': 'Bus', 'cost': 10, 'time': '30 mins'},
            {'mode': 'Train', 'cost': 20, 'time': '15 mins'},
            {'mode': 'Car', 'cost': 15, 'time': '25 mins'}
        ]

    def save_trip_options(self, username: str = None, options: list = None) -> None:
        with open('trips.txt', 'a') as file:
            for trip in self.trips:
                file.write(f"{trip['start']}|{trip['destination']}|{trip['date']}\n")

    def load_trips(self) -> None:
        if os.path.exists('trips.txt'):
            with open('trips.txt', 'r') as file:
                for line in file:
                    start, destination, date = line.strip().split('|')
                    self.trips.append({'start': start, 'destination': destination, 'date': date})

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if app.user_manager.register(username, password):
            flash('Registration successful!')
            return redirect(url_for('login'))
        else:
            flash('Username already exists!')
    return render_template('register.html')

@app.route('/trip_input', methods=['GET', 'POST'])
def trip_input():
    if request.method == 'POST':
        start = request.form['start']
        destination = request.form['destination']
        date = request.form['date']
        app.trip_manager.add_trip(start, destination, date)
        options = app.trip_manager.get_transportation_options(start, destination, date)
        return render_template('results.html', options=options)
    return render_template('trip_input.html')

if __name__ == '__main__':
    main_app = Main()
    main_app.main()