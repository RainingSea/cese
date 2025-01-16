from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from trip import Trip
from transportation_option import TransportationOption
from trip_saver import TripSaver

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production
trip_saver = TripSaver()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        trip_saver.register(username, password)
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if trip_saver.login(username, password):
        session['username'] = username
        return redirect(url_for('trip_input'))
    return redirect(url_for('login'))

@app.route('/trip_input', methods=['GET', 'POST'])
def trip_input():
    if request.method == 'POST':
        starting_point = request.form['starting_point']
        destination = request.form['destination']
        travel_date = request.form['travel_date']
        trip_saver.input_trip(starting_point, destination, travel_date)
        return redirect(url_for('suggestions'))
    return render_template('trip_input.html')

@app.route('/suggestions')
def suggestions():
    suggestions = trip_saver.get_suggestions()
    return render_template('suggestions.html', suggestions=suggestions)

@app.route('/comparison')
def comparison():
    options = trip_saver.compare_options()
    return render_template('comparison.html', options=options)

@app.route('/saved_options')
def saved_options():
    saved_options = trip_saver.suggestions
    return render_template('saved_options.html', saved_options=saved_options)

if __name__ == '__main__':
    app.run(port=8680, debug=False)
