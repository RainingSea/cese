from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from trip import Trip
from transportation_option import TransportationOption
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

class TripSaverApp:
    def __init__(self):
        self.users = self.load_users()
        self.trips = self.load_trips()
        self.options = self.load_options()

    def load_users(self):
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def load_trips(self):
        trips = []
        if os.path.exists('trips.txt'):
            with open('trips.txt', 'r') as file:
                for line in file:
                    starting_point, destination, travel_date = line.strip().split('|')
                    trips.append(Trip(starting_point, destination, travel_date))
        return trips

    def load_options(self):
        options = []
        if os.path.exists('options.txt'):
            with open('options.txt', 'r') as file:
                for line in file:
                    type_, cost, time = line.strip().split('|')
                    options.append(TransportationOption(type_, float(cost), float(time)))
        return options

    def register(self, username: str, password: str):
        new_user = User(username, password)
        self.users.append(new_user)
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

    def input_trip(self, starting_point: str, destination: str, travel_date: str):
        new_trip = Trip(starting_point, destination, travel_date)
        self.trips.append(new_trip)
        with open('trips.txt', 'a') as file:
            file.write(f"{starting_point}|{destination}|{travel_date}\n")

    def get_transportation_options(self):
        return self.options

    def compare_options(self):
        return self.options

    def save_preferred_options(self, option: TransportationOption):
        with open('options.txt', 'a') as file:
            file.write(f"{option.type}|{option.cost}|{option.time}\n")

trip_saver_app = TripSaverApp()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        trip_saver_app.register(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/trip_input', methods=['GET', 'POST'])
def trip_input():
    if request.method == 'POST':
        starting_point = request.form['starting_point']
        destination = request.form['destination']
        travel_date = request.form['travel_date']
        trip_saver_app.input_trip(starting_point, destination, travel_date)
        return redirect(url_for('results'))
    return render_template('trip_input.html')

@app.route('/results')
def results():
    options = trip_saver_app.get_transportation_options()
    return render_template('results.html', options=options)

@app.route('/comparison')
def comparison():
    options = trip_saver_app.compare_options()
    return render_template('comparison.html', options=options)

@app.route('/saved_options')
def saved_options():
    return render_template('saved_options.html')

if __name__ == '__main__':
    app.run(port=8679, debug=False)
