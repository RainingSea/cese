from flask import Flask, render_template, request, redirect, url_for, session
from typing import List
import os

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class Trip:
    def __init__(self, starting_point: str, destination: str, travel_date: str):
        self.starting_point = starting_point
        self.destination = destination
        self.travel_date = travel_date

class TransportationOption:
    def __init__(self, mode: str, cost: float, time: float):
        self.mode = mode
        self.cost = cost
        self.time = time

class TripSaverApp:
    def __init__(self):
        self.users = self.load_users()
        self.trips = self.load_trips()
        self.preferences = self.load_preferences()

    def load_users(self) -> List[User]:
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def load_trips(self) -> List[Trip]:
        trips = []
        if os.path.exists('trips.txt'):
            with open('trips.txt', 'r') as file:
                for line in file:
                    starting_point, destination, travel_date = line.strip().split('|')
                    trips.append(Trip(starting_point, destination, travel_date))
        return trips

    def load_preferences(self) -> List[TransportationOption]:
        preferences = []
        if os.path.exists('preferences.txt'):
            with open('preferences.txt', 'r') as file:
                for line in file:
                    mode, cost, time = line.strip().split('|')
                    preferences.append(TransportationOption(mode, float(cost), float(time)))
        return preferences

    def register(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        self.users.append(User(username, password))
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user.username == username and user.password == password for user in self.users)

    def input_trip(self, starting_point: str, destination: str, travel_date: str) -> List[TransportationOption]:
        # Dummy transportation options for demonstration
        return [
            TransportationOption("Bus", 10.0, 30.0),
            TransportationOption("Train", 20.0, 15.0),
            TransportationOption("Flight", 100.0, 120.0)
        ]

    def save_preference(self, option: TransportationOption) -> None:
        self.preferences.append(option)
        with open('preferences.txt', 'a') as file:
            file.write(f"{option.mode}|{option.cost}|{option.time}\n")

    def logout(self) -> None:
        session.pop('username', None)

app = Flask(__name__)
app.secret_key = 'your_secret_key'
trip_saver_app = TripSaverApp()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if trip_saver_app.register(username, password):
            return redirect(url_for('home'))
        else:
            return "Username already exists!"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if trip_saver_app.login(username, password):
            session['username'] = username
            return redirect(url_for('trip_input'))
        else:
            return "Invalid credentials!"
    return render_template('login.html')

@app.route('/trip_input', methods=['GET', 'POST'])
def trip_input():
    if request.method == 'POST':
        starting_point = request.form['starting_point']
        destination = request.form['destination']
        travel_date = request.form['travel_date']
        options = trip_saver_app.input_trip(starting_point, destination, travel_date)
        return render_template('results.html', options=options)
    return render_template('trip_input.html')

@app.route('/logout')
def logout():
    trip_saver_app.logout()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=8678, debug=False)
