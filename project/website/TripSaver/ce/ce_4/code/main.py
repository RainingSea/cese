from flask import Flask, request, redirect, render_template, session
from user import User
from trip import Trip
from auth import Auth

app = Flask(__name__)
app.secret_key = 'your_secret_key'

auth = Auth()
trip = Trip()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.login(username, password):
            session['username'] = username
            return redirect('/trip_input')
        return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth.register(username, password):
            return redirect('/')
        return "Registration failed", 400
    return render_template('register.html')

@app.route('/trip_input', methods=['GET', 'POST'])
def trip_input():
    if 'username' not in session:
        return redirect('/')
    
    if request.method == 'POST':
        starting_point = request.form['starting_point']
        destination = request.form['destination']
        travel_date = request.form['travel_date']
        trip = Trip(starting_point, destination, travel_date)
        trip.save_trip()
        return "Trip saved successfully", 200
    return render_template('trip_input.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8681, debug=False)
