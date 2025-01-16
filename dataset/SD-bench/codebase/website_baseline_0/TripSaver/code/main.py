from flask import Flask, render_template, request, redirect, url_for, session, flash
from user import User
from trip import Trip
from saved_option import SavedOption
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from file
def load_users():
    users = {}
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users[username] = password
    return users

# Load trips from file
def load_trips():
    trips = []
    if os.path.exists('trips.txt'):
        with open('trips.txt', 'r') as f:
            for line in f:
                starting_point, destination, travel_date = line.strip().split('|')
                trips.append(Trip(starting_point, destination, travel_date))
    return trips

# Load saved options from file
def load_saved_options():
    saved_options = {}
    if os.path.exists('saved_options.txt'):
        with open('saved_options.txt', 'r') as f:
            for line in f:
                user, options = line.strip().split('|')
                saved_options[user] = options.split(',')
    return saved_options

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))
        user = User(username, password)
        user.save()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('trip_input'))
    flash('Invalid username or password. Please try again.')
    return redirect(url_for('login'))

@app.route('/trip_input', methods=['GET', 'POST'])
def trip_input():
    if request.method == 'POST':
        starting_point = request.form['starting_point']
        destination = request.form['destination']
        travel_date = request.form['travel_date']
        
        # Validate input fields
        if not starting_point or not destination or not travel_date:
            flash('All fields are required.')
            return redirect(url_for('trip_input'))

        trip = Trip(starting_point, destination, travel_date)
        trip.save()
        return redirect(url_for('suggestions'))
    return render_template('trip_input.html')

@app.route('/suggestions')
def suggestions():
    trips = load_trips()
    suggestions = []
    for trip in trips:
        suggestions.extend(trip.get_suggestions())
    return render_template('suggestions.html', suggestions=suggestions)

@app.route('/comparison', methods=['GET', 'POST'])
def comparison():
    trips = load_trips()
    comparison_data = []
    for trip in trips:
        comparison_data.append({
            "starting_point": trip.starting_point,
            "destination": trip.destination,
            "travel_date": trip.travel_date,
            "suggestions": trip.get_suggestions()
        })
    return render_template('comparison.html', comparison_data=comparison_data)

@app.route('/saved_options', methods=['GET', 'POST'])
def saved_options():
    if request.method == 'POST':
        user = session.get('username')
        options = request.form.getlist('options')
        saved_option = SavedOption(user, options)
        saved_option.save()
        flash('Options saved successfully!')
        return redirect(url_for('saved_options'))

    saved_options = load_saved_options()
    return render_template('saved_options.html', saved_options=saved_options)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8561, debug=False)
