from flask import Flask, render_template, request, redirect, url_for, flash
from flask_httpauth import HTTPBasicAuth
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
auth = HTTPBasicAuth()

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        if self.check_duplicate(username):
            return False
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        self.users[username] = password
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def check_duplicate(self, username: str) -> bool:
        return username in self.users

class TripManager:
    def __init__(self, trips_file: str):
        self.trips_file = trips_file
        self.load_trips()

    def load_trips(self):
        self.trips = []
        if os.path.exists(self.trips_file):
            with open(self.trips_file, 'r') as file:
                for line in file:
                    self.trips.append(line.strip().split(':'))

    def save_trip(self, username: str, start_point: str, end_point: str, travel_date: str, transport_option: str) -> bool:
        with open(self.trips_file, 'a') as file:
            file.write(f"{username}:{start_point}:{end_point}:{travel_date}:{transport_option}\n")
        return True

    def get_transport_options(self, start_point: str, end_point: str, travel_date: str) -> list:
        return [
            {"option": "Bus", "cost": 10, "time": "1h 30m"},
            {"option": "Train", "cost": 20, "time": "1h"},
            {"option": "Car", "cost": 15, "time": "1h 15m"}
        ]

    def compare_options(self, options: list) -> str:
        comparison = "Estimated Costs and Travel Times:\n"
        for option in options:
            comparison += f"{option['option']} - Cost: ${option['cost']}, Time: {option['time']}\n"
        return comparison

user_manager = UserManager('users.txt')
trip_manager = TripManager('trips.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect(url_for('trip_input', username=username))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful!')
            return redirect(url_for('login'))
        else:
            flash('Username already exists.')
            return render_template('registration.html')  # Render registration page again with error message
    return render_template('registration.html')

@app.route('/trip_input', methods=['GET', 'POST'])
def trip_input():
    username = request.args.get('username')
    if request.method == 'POST':
        start_point = request.form['start_point']
        end_point = request.form['end_point']
        travel_date = request.form['travel_date']
        transport_option = request.form['transport_option']
        trip_manager.save_trip(username, start_point, end_point, travel_date, transport_option)
        flash('Trip details saved!')
        return redirect(url_for('suggestions', start_point=start_point, end_point=end_point, travel_date=travel_date))
    return render_template('trip_input.html', username=username)

@app.route('/suggestions')
def suggestions():
    start_point = request.args.get('start_point')
    end_point = request.args.get('end_point')
    travel_date = request.args.get('travel_date')
    options = trip_manager.get_transport_options(start_point, end_point, travel_date)
    return render_template('suggestions.html', options=options)

@app.route('/comparison')
def comparison():
    start_point = request.args.get('start_point')
    end_point = request.args.get('end_point')
    travel_date = request.args.get('travel_date')
    options = trip_manager.get_transport_options(start_point, end_point, travel_date)
    comparison = trip_manager.compare_options(options)
    return render_template('comparison.html', comparison=comparison)

@app.route('/logout')
def logout():
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8277, debug=False)
