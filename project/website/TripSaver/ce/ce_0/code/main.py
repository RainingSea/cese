from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class UserManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file

    def register(self, username, password):
        with open(self.users_file, 'a') as f:
            f.write(f"{username},{password}\n")
        return True

    def login(self, username, password):
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    stored_user, stored_pass = line.strip().split(',')
                    if stored_user == username and stored_pass == password:
                        return True
        except FileNotFoundError:
            return False
        return False

class TripManager:
    def __init__(self, trips_file='trips.txt'):
        self.trips_file = trips_file
        self.mock_options = {
            ('New York', 'Boston'): [
                {'type': 'Train', 'cost': 50, 'time': '4 hours'},
                {'type': 'Bus', 'cost': 30, 'time': '5 hours'},
                {'type': 'Flight', 'cost': 120, 'time': '1 hour'}
            ],
            ('Chicago', 'Detroit'): [
                {'type': 'Train', 'cost': 40, 'time': '3 hours'},
                {'type': 'Bus', 'cost': 25, 'time': '4 hours'},
                {'type': 'Flight', 'cost': 150, 'time': '1 hour'}
            ]
        }

    def get_options(self, start, end):
        key = (start, end)
        return self.mock_options.get(key, [])

    def save_preference(self, username, trip_data):
        with open(self.trips_file, 'a') as f:
            f.write(f"{username},{trip_data['start']},{trip_data['destination']},{trip_data['date']},{trip_data['type']},{trip_data['cost']},{trip_data['time']}\n")
        return True

user_manager = UserManager()
trip_manager = TripManager()

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('trip_input'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('trip_input'))
    return render_template('login.html')

@app.route('/trip', methods=['GET', 'POST'])
def trip_input():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        start = request.form['start']
        destination = request.form['destination']
        date = request.form['date']
        return redirect(url_for('results', start=start, destination=destination, date=date))
    return render_template('trip_input.html')

@app.route('/results')
def results():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    start = request.args.get('start')
    destination = request.args.get('destination')
    date = request.args.get('date')
    options = trip_manager.get_options(start, destination)
    
    return render_template('results.html', 
                         options=options, 
                         start=start, 
                         destination=destination, 
                         date=date)

@app.route('/save_trip', methods=['POST'])
def save_trip():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    trip_data = {
        'start': request.form['start'],
        'destination': request.form['destination'],
        'date': request.form['date'],
        'type': request.form['type'],
        'cost': request.form['cost'],
        'time': request.form['time']
    }
    trip_manager.save_preference(session['username'], trip_data)
    return redirect(url_for('trip_input'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8075, debug=False)
