from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.trip_manager = TripManager()

    def main(self):
        self.user_manager.load_users()
        self.trip_manager.load_trips()
        app.run(port=8274, debug=False)

class UserManager:
    def __init__(self):
        self.users = []

    def register(self, username: str, password: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        self.users.append({'username': username, 'password': password})
        self.save_users()
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user['username'] == username and user['password'] == password for user in self.users)

    def load_users(self) -> None:
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users.append({'username': username, 'password': password})
        except FileNotFoundError:
            pass

    def save_users(self) -> None:
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user['username']}|{user['password']}\n")

class TripManager:
    def __init__(self):
        self.trips = []

    def add_trip(self, start: str, destination: str, date: str) -> None:
        trip = {'start': start, 'destination': destination, 'date': date}
        self.trips.append(trip)
        self.save_trip(trip)

    def get_suggestions(self, start: str, destination: str, date: str) -> list:
        # Placeholder for suggestion logic
        return [{'option': 'Bus', 'cost': 20, 'time': '2h'}, {'option': 'Train', 'cost': 30, 'time': '1.5h'}]

    def save_trip(self, trip: dict) -> None:
        with open('trips.txt', 'a') as file:
            file.write(f"{trip['start']}|{trip['destination']}|{trip['date']}\n")

    def load_trips(self) -> None:
        try:
            with open('trips.txt', 'r') as file:
                for line in file:
                    start, destination, date = line.strip().split('|')
                    self.trips.append({'start': start, 'destination': destination, 'date': date})
        except FileNotFoundError:
            pass

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if Main().user_manager.register(username, password):
            return redirect('/')
    return render_template('registration.html')

@app.route('/trip_input', methods=['GET', 'POST'])
def trip_input():
    if request.method == 'POST':
        start = request.form['start']
        destination = request.form['destination']
        date = request.form['date']
        Main().trip_manager.add_trip(start, destination, date)
        return redirect('/suggestions')
    return render_template('trip_input.html')

@app.route('/suggestions')
def suggestions():
    return render_template('suggestions.html', suggestions=Main().trip_manager.get_suggestions('', '', ''))

if __name__ == '__main__':
    Main().main()