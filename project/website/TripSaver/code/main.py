from flask import Flask, render_template, request, redirect, session
from user import User
from trip import Trip
from transportation_option import TransportationOption
from trip_saver import TripSaver

app = Flask(__name__)
app.secret_key = 'your_secret_key'

trip_saver = TripSaver()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if trip_saver.login_user(username, password):
            session['username'] = username
            return redirect('/trip_input')
        else:
            return render_template('login.html', error="Invalid username or password!")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if trip_saver.register_user(username, password):
            return redirect('/')
        else:
            return render_template('register.html', error="Username already exists!")
    return render_template('register.html')

@app.route('/trip_input', methods=['GET', 'POST'])
def trip_input():
    if request.method == 'POST':
        starting_point = request.form['starting_point']
        destination = request.form['destination']
        travel_date = request.form['travel_date']
        trip_saver.input_trip(starting_point, destination, travel_date)
        return redirect('/comparison')
    return render_template('trip_input.html')

@app.route('/comparison', methods=['GET', 'POST'])
def comparison():
    options = trip_saver.get_transportation_options()
    estimated_costs = trip_saver.calculate_estimated_costs(options)
    if request.method == 'POST':
        preferred_option = request.form['preferred_option']
        trip_saver.save_preferred_transportation_option(session['username'], preferred_option)
        return redirect('/comparison')
    return render_template('comparison.html', options=options, estimated_costs=estimated_costs)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8682, debug=False)
