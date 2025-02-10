from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from trip import Trip
from option import Option
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load data from files
def load_users():
    users = []
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users.append(User(username, password))
    return users

def load_trips():
    trips = []
    if os.path.exists('trips.txt'):
        with open('trips.txt', 'r') as f:
            for line in f:
                starting_point, destination, travel_date = line.strip().split('|')
                trips.append(Trip(starting_point, destination, travel_date))
    return trips

def load_options():
    options = []
    if os.path.exists('options.txt'):
        with open('options.txt', 'r') as f:
            for line in f:
                mode, cost, time = line.strip().split('|')
                options.append(Option(mode, float(cost), float(time)))
    return options

users = load_users()
trips = load_trips()
options = load_options()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        users.append(new_user)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/trip_input', methods=['GET', 'POST'])
def trip_input():
    if request.method == 'POST':
        starting_point = request.form['starting_point']
        destination = request.form['destination']
        travel_date = request.form['travel_date']
        new_trip = Trip(starting_point, destination, travel_date)
        trips.append(new_trip)
        new_trip.save()
        return redirect(url_for('suggest_options'))
    return render_template('trip_input.html')

@app.route('/suggest_options')
def suggest_options():
    return render_template('suggestions.html', options=options)

@app.route('/comparison')
def comparison():
    return render_template('comparison.html', options=options)

@app.route('/save_options', methods=['POST'])
def save_options():
    selected_option = request.form['selected_option']
    for option in options:
        if option.mode == selected_option:
            option.save()
            break
    return redirect(url_for('suggest_options'))

if __name__ == '__main__':
    app.run(port=8677, debug=False)
